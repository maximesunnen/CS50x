DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS parent;
DROP TABLE IF EXISTS parent_child;

-- Table to store user (child) information
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  password TEXT NOT NULL,
  birthday DATE NOT NULL,
  gender TEXT NOT NULL,
  allergies TEXT,
  diet TEXT,
  branch TEXT,
  otherInformation TEXT,
  scout_registration TEXT DEFAULT 'FALSE'
);

-- Table to store the address of the user
CREATE TABLE address (
  address_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  house_number TEXT NOT NULL,
  street TEXT NOT NULL,
  town TEXT NOT NULL,
  country TEXT NOT NULL,
  zip INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Table to store information on child's parent
CREATE TABLE parent (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
);

-- Junction table with composite key
/* 
composite key: the combination of (parent_id, child_id) must be unique. For example (2,1) cannot be in the same table twice.
junction table: create a many-to-many relationship between entitities (one parent -> many users, one user -> many (>1, usually) parents)
*/

CREATE TABLE parent_child (
  parent_id INTEGER NOT NULL,
  child_id INTEGER NOT NULL,
  PRIMARY KEY (parent_id, child_id),
  FOREIGN KEY (parent_id) REFERENCES parent (id),
  FOREIGN KEY (child_id) REFERENCES user (id)
);