-- Data cleaning with SQL

SELECT * 
FROM dbo.Nashville


-- standarding date

SELECT SaleDate, CONVERT(DATE,SaleDate)
FROM dbo.Nashville

Update Nashville
Set SaleDate = CONVERT(DATE,SaleDate)

ALTER TABLE Nashville
Add SaleDateConverted DATE;

UPDATE Nashville
SET SaleDateConverted = CONVERT(DATE, SaleDate)


--- Populate Property Address data

SELECT *
FROM dbo.Nashville
ORDER BY ParcelID

-- self join to determine where property address is the same based on having a similar parcel ID

SELECT a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.propertyAddress, b.PropertyAddress)
FROM dbo.Nashville a
JOIN dbo.Nashville b
    on a.parcelID = b.ParcelID
	AND a.UniqueID <> b.UniqueID
WHERE a.PropertyAddress IS NULL

-- updating table to fill in null Prpert Addresses
UPDATE a
SET PropertyAddress = ISNULL(a.propertyAddress, b.PropertyAddress)
FROM dbo.Nashville a
JOIN dbo.Nashville b
    on a.parcelID = b.ParcelID
	AND a.UniqueID <> b.UniqueID
WHERE a.PropertyAddress IS NULL

--Spliting address into columns

-- Property Address includes city and must be split. Will use substring method for Property Address


SELECT
SUBSTRING(PropertyAddress, 1, CHARINDEX(',',PropertyAddress) -1) as Address,
SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress) +1, LEN(PropertyAddress)) as City

FROM dbo.Nashville


-- Alter tables to seperate address from City
ALTER TABLE Nashville
Add PropertySplitAddress NVARCHAR(255);

ALTER TABLE Nashville
Add PropertySplitCity NVARCHAR(255);


UPDATE Nashville
SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',',PropertyAddress) -1)


UPDATE Nashville
SET PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress) +1, LEN(PropertyAddress))


-- Owner Address will be split using parsename method 

SELECT OwnerAddress
FROM dbo.Nashville

SELECT
PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3),
PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2),
PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)
FROM dbo.Nashville


-- Altering Property owner table
ALTER TABLE Nashville
Add OwnerSplitAddress NVARCHAR(255);

ALTER TABLE Nashville
Add OwnerSplitCity NVARCHAR(255);

ALTER TABLE Nashville
Add OwnerSplitState NVARCHAR(255);


UPDATE Nashville
SET OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3)


UPDATE Nashville
SET OwnerSplitCity = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2)


UPDATE Nashville
SET OwnerSplitState = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)

--change 0 and 1 to Yes and No in sold as cvacant field

Select SoldAsVacant
FROM dbo.Nashville


SELECT DISTINCT(SoldAsVacant), COUNT(SoldAsVacant)
FROM dbo.nashville
GROUP BY SoldAsVacant
Order By 2


SELECT SoldAsVacant,
    CASE When SoldAsVacant = '0' THEN 'No'
	ELSE 'Yes'
	END
FROM dbo.nashville

UPDATE Nashville
SET SoldAsVacant =  
     CASE When SoldAsVacant = '0' THEN 'No'
	ELSE 'Yes'
	END


SELECT SoldAsVacant FROM dbo.Nashville

-- remove duplicants using row_number to determine where row_number is greater than 1 
WITH RowNumCTE AS(
SELECT *,
     ROW_NUMBER() OVER (
	 PARTITION BY ParcelID,
	 PropertyAddress, 
	 SalePrice, 
	 SaleDate,
	 LegalReference
     ORDER BY
	    UniqueID
		) row_num
FROM dbo.Nashville
)
DELETE
FROM RowNumCTE
WHERE row_num > 1


-- delete unused columns

SELECT * 
FROM dbo.Nashville

-- drop columns that are not needed. SaleDate, Owner Address and propertyAddress were split and usable in seperate columns. Tax District in not needed. 
ALTER TABLE dbo.Nashville
DROP COLUMN  OwnerAddress, TaxDistrict, SaleDate, PropertyAddress