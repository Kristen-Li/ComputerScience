
CREATE TABLE Sale (
  saleID INT(16) UNSIGNED NOT NULL AUTO_INCREMENT,
  fk_sale_store_number INT(16) UNSIGNED NOT NULL,
  fk_sale_PID INT(16) UNSIGNED NOT NULL,
  fk_sale_date DATE NOT NULL,
  quantity INT(16) UNSIGNED NOT NULL,
  PRIMARY KEY (saleID)
);

CREATE TABLE Childcare (
  childcareID INT(16) UNSIGNED NOT NULL,
  time_limit INT(8) NOT NULL,
  PRIMARY KEY (childcareID)
);

CREATE TABLE `Date` (
`date` DATE NOT NULL,
PRIMARY KEY (`date`)
);
 
CREATE TABLE AdCampaign(
campaignID INT(16) UNSIGNED NOT NULL AUTO_INCREMENT,
`description` VARCHAR(250) NOT NULL,
PRIMARY KEY (campaignID),
UNIQUE KEY (`description`)
);
 
CREATE TABLE Holiday(
fk_holiday_date DATE NOT NULL,
`name` VARCHAR(250) NOT NULL,
PRIMARY KEY (fk_holiday_date)
);

CREATE TABLE City (
    cityID INT(16) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(250) NOT NULL,
    state VARCHAR(250) NOT NULL,
    population LONG NOT NULL,
    PRIMARY KEY (cityID)
);

CREATE TABLE Store (
    store_number INT(16) NOT NULL AUTO_INCREMENT,
    phone_number VARCHAR(250) NOT NULL,
    street_address VARCHAR(250) NOT NULL,
    snack_bar  BOOLEAN NOT NULL,
    restaurant BOOLEAN NOT NULL,
    fk_store_cityID INT(16) NOT NULL,
    fk_store_childcareID INT(16),
    PRIMARY KEY(store_number)
);

CREATE TABLE BelongsTo(
fk_belongsto_PID VARCHAR(12) NOT NULL,
fk_belongsto_category_name VARCHAR(100) NOT NULL,
PRIMARY KEY (fk_belongsto_PID, fk_belongsto_category_name)
);

CREATE TABLE Category(
`name` VARCHAR(250) NOT NULL,
PRIMARY KEY (`name`)
);

CREATE TABLE EventDate(
fk_eventdate_campaignID INT(16) UNSIGNED NOT NULL,
fk_eventdate_date DATE NOT NULL,
PRIMARY KEY (fk_eventdate_campaignID,fk_eventdate_date)
);

CREATE TABLE Product (
PID VARCHAR(12) NOT NULL,
`name` VARCHAR (100) NOT NULL,
retail_price DECIMAL(19, 2) NOT NULL,
PRIMARY KEY (PID)
);

CREATE TABLE Discount (
discountID INT(16) UNSIGNED NOT NULL,
fk_discount_PID VARCHAR(12) NOT NULL,
fk_discount_date DATE NOT NULL,
discount_price DECIMAL(19, 2) NOT NULL,
PRIMARY KEY (discountID)
);

-- constraints

ALTER TABLE Sale
  ADD CONSTRAINT fk_Sale_storenumber_Store_storenumber FOREIGN KEY (fk_sale_store_number) REFERENCES Store (store_number),
  ADD CONSTRAINT fk_Sale_fkPID_Product_PID FOREIGN KEY (fk_sale_PID) REFERENCES Product (PID),
  ADD CONSTRAINT fk_Sale_fkdate_Date_date FOREIGN KEY (fk_sale_date) REFERENCES `Date` (`date`);

ALTER TABLE Discount
  ADD CONSTRAINT fk_Discount_date_Date_date FOREIGN KEY (fk_discount_date) REFERENCES `Date`(`date`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT fk_Discount_PID_Product_PID FOREIGN KEY (fk_discount_PID) REFERENCES Product(PID) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Holiday
  ADD CONSTRAINT fk_Holiday_date_Date_date FOREIGN KEY (fk_holiday_date) REFERENCES `Date` (`date`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE EventDate
  ADD CONSTRAINT fk_EventDate_eventdate_campaignID_AdCampaign_campaignID FOREIGN KEY (fk_eventdate_campaignID) REFERENCES AdCampaign(campaignID) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT fk_EventDate_eventdate_date_Date_date FOREIGN KEY (fk_eventdate_date) REFERENCES `Date`(`date`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE BelongsTo
  ADD CONSTRAINT fk_BelongsTo_belongsto_PID_Product_PID FOREIGN KEY (fk_belongsto_PID) REFERENCES Product(PID) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT fk_BelongsTo_belongsto_category_name_Category_name FOREIGN KEY (fk_belongsto_category_name) REFERENCES Category(`name`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE Store
  ADD CONSTRAINT fk_store_cityID_city_cityID FOREIGN KEY (fk_store_cityID) REFERENCES City (cityID) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT fk_store_childcareID_Childcare_childcareID FOREIGN KEY (fk_store_childcareID) REFERENCES Childcare(childcareID) ON DELETE SET NULL ON UPDATE CASCADE;