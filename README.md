# CommunityShelf
Web application; facilitates borrowing useful goods to people in your community

### Stored procedures:
CREATE PROCEDURE `GetUserIdByUsername`( IN input_username VARCHAR(255), OUT output_userId INT)
BEGIN
    DECLARE user_id_result INT;


    SELECT userId INTO user_id_result
    FROM users
    WHERE name = input_username;


    SET output_userId = user_id_result;
END 

Create proCEDURE `CreateUser`(
    IN input_username VARCHAR(255),
    IN input_email VARCHAR(255),
    IN input_phone_number VARCHAR(15),
    IN input_address VARCHAR(255),
    IN input_zip VARCHAR(10),
    IN input_password VARCHAR(255)
)
BEGIN
    DECLARE user_count INT;

    SELECT COUNT(*) INTO user_count
    FROM users
    WHERE name = input_username;

    -- If the username doesn't exist, insert a new row
    IF user_count = 0 THEN
        INSERT INTO users (name, email, phoneNumber, address, zip, password)
        VALUES (input_username, input_email, input_phone_number, input_address, input_zip, input_password);

        SELECT 'Successful' AS result;
    ELSE
        SELECT 'Unsuccessful' AS result;
    END IF;
END 



CREATE PROCEDURE `GetItemDetails`(
    IN input_itemId INT,
    OUT output_name VARCHAR(50),
    OUT output_category_id INT,
    OUT output_retail_cost DECIMAL(10, 2),
    OUT output_description VARCHAR(300)
)
BEGIN
    DECLARE item_name VARCHAR(50);
    DECLARE category_id_result INT;
    DECLARE retail_cost_result INT;
    DECLARE item_description VARCHAR(300);

    SELECT name, category_id, retail_cost, description
    INTO item_name, category_id_result, retail_cost_result, item_description
    FROM items
    WHERE itemId = input_itemId;

    SET output_name = item_name;
    SET output_category_id = category_id_result;
    SET output_retail_cost = retail_cost_result;
    SET output_description = item_description;
END 



### Database implementation notes
users: 
+-------------+--------------+------+-----+-------------------+-------------------+

| Field       | Type         | Null | Key | Default           | Extra             |

+-------------+--------------+------+-----+-------------------+-------------------+

| userId      | int          | NO   | PRI | NULL              | auto_increment    |

| name        | varchar(50)  | YES  |     | NULL              |                   |

| email       | varchar(70)  | YES  |     | NULL              |                   |

| phoneNumber | varchar(20)  | YES  |     | NULL              |                   |

| createdAt   | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

| address     | varchar(100) | YES  |     | NULL              |                   |

| zip         | int          | YES  | MUL | NULL              |                   |

| password    | varchar(50)  | YES  |     | NULL              |                   |

+-------------+--------------+------+-----+-------------------+-------------------+
    
items: 

+-------------+--------------+------+-----+---------+----------------+

| Field       | Type         | Null | Key | Default | Extra          |

+-------------+--------------+------+-----+---------+----------------+

| itemId      | int          | NO   | PRI | NULL    | auto_increment |

| ownerId     | int          | YES  | MUL | NULL    |                |

| name        | varchar(50)  | YES  |     | NULL    |                |

| category_id | int          | YES  | MUL | NULL    |                |

| retail_cost | int          | YES  |     | NULL    |                |

| description | varchar(300) | YES  |     | NULL    |                |

+-------------+--------------+------+-----+---------+----------------+



categories:
    *categoryId INTEGER*,
    category VARCHAR(30)

### creating categories table
INSERT INTO categories (categoryId, category) VALUES
(1, 'Kitchen'),
(2, 'Landscaping'),
(3, 'Miscellaneous'),
(4, 'Party Supplies');


    
