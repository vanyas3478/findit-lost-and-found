-- SQL examples for classroom explanation
-- Open the website and use its forms to add records.
-- These examples explain the SQL commands used by the app.

-- 1. Show all items
SELECT * FROM items;

-- 2. Find lost items
SELECT * FROM items WHERE item_type = 'Lost';

-- 3. Search item names that contain "ID"
SELECT * FROM items WHERE title LIKE '%ID%';

-- 4. Show item reports with the name of the reporting user
SELECT items.title, items.item_type, users.name
FROM items
JOIN users ON items.user_id = users.id;

-- 5. Change an item's status (replace 1 with an actual item id)
UPDATE items SET status = 'Resolved' WHERE id = 1;

-- 6. Count the number of reports
SELECT COUNT(*) FROM items;
