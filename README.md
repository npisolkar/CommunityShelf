# CommunityShelf
Web application; facilitates borrowing useful goods to people in your community


### Database implementation notes
users: 
    *userId INTEGER*, 
    name VARCHAR(50), 
    phone_number VARCHAR(20), 
    email VARCHAR(50)
    
items: 
    *itemId INTEGER*, 
    ownerId INTEGER references users (userId)
    name VARCHAR(50), 
    category_id INTEGER references categories (categoryId), 
    retail_cost INTEGER, 
    description VARCHAR(300)
    
loans:  
    *borrowerId INTEGER references users (userId),
    itemId INTEGER references items (itemId),
    startDate date,*
    endDate data

categories:
    *categoryId INTEGER*,
    category VARCHAR(30)
    
