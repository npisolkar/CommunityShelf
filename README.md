# CommunityShelf
Web application; facilitates borrowing useful goods to people in your community


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
    
