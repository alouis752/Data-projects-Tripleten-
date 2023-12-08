# Nashville Housing


This project utilized SQL to clean data regarding Nashville housing. This dataset included messy factors such as the date not being standardized, Addresses including all info in 1 field, and duplicate rows.



My first step in this project was to standardize the date. The initial format included the date and the time. The time was unnecessary, so I isolated the date using the following statements: 

	ALTER TABLE Nashville
	Add SaleDateConverted DATE;
	
	UPDATE Nashville
	SET SaleDateConverted = CONVERT(DATE, SaleDate)

The alter table statement adds an additional column to the end of the dataset. This prevents any mistakes from happening while overwriting necessary data. Once the new column is created, the sales date is converted to the date and written to the created column

The next step was to fill in empty property addresses. It was assumed that 2 parcel IDs that are identical would be delivered to the same address. Using this information, the following code was used to populate the missing fields:

	UPDATE a
	SET PropertyAddress = ISNULL(a.propertyAddress, b.PropertyAddress)
	FROM dbo.Nashville a
	JOIN dbo.Nashville b
	    on a.parcelID = b.ParcelID
		AND a.UniqueID <> b.UniqueID
	WHERE a.PropertyAddress IS NULL

By joining the data on itself I can compare the columns where parcel id is the same value but the unique ID is not. This was used to set the null values to that which is in the corresponding parcel ID field


I then split the address fields into separate columns. In the original data, the field was combined as "address,city" and "address,city,state". To make analysis easier, The data was split into seperate columns. This was done in 2 different ways:

To handle the property address, which was formatted as "address,city" the substring statement was used:

	ALTER TABLE Nashville
	Add PropertySplitAddress NVARCHAR(255);
	
	ALTER TABLE Nashville
	Add PropertySplitCity NVARCHAR(255);
	
	UPDATE Nashville
	SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',',PropertyAddress) -1)
	
	UPDATE Nashville
	SET PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress) +1, LEN(PropertyAddress))

This statement separates the data at the delimiter, in this case the ",". A "-1" or "+1" were used to determine where to start and end the splits.

For the owner address, which was formatted as "address,city,state", parsename was used instead.

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

Using parcename, the "," was replaced to a "." Parcename naturally splits data at the "." so once replaced, it made the job easier than the previous method. Note that parsename splits the text starrting with the last value, so updates were assigned starting at 3 and ending at 1.


The next step was to take care of the Sold as Vacant column. This column should read "Yes" or "No" but the data was set as 0 or 1.
This was overcome with the statement:

	UPDATE Nashville
	SET SoldAsVacant =  
	     CASE When SoldAsVacant = '0' THEN 'No'
		ELSE 'Yes'
		END

Using a case statement, values were changed to be easier for a viewer to read.

The next step was to remove duplicate columns. Through analysis, multiple rows had the same data as the one before it. To remedy this, the row_number window function was utilized:

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


Row_number was used to count how many rows were the same as the one before it. Using this information, rows were deleted where the row number was greater than 1

The last step was to delete unnecessary columns. This was done using the delete command:

	ALTER TABLE dbo.Nashville
	DROP COLUMN  OwnerAddress, TaxDistrict, SaleDate, PropertyAddress


OwnderAddress, SaleDate, and Property Address were previously split into new columns. TaxDistrict was decided to be unnecessary.


In the future, I plan on diving into this data more and turning it into a visualization with the goal of answering questions such as if most property owners live in the property and which addresses sold for the greatest amount of money based on size and location


