DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS parent1;
DROP TABLE IF EXISTS parent2;

-- Table to store user (child) information
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  password TEXT NOT NULL,
  birthdate DATE NOT NULL,
  sex TEXT NOT NULL,
  nationality TEXT NOT NULL,
  allergies TEXT,
  diet TEXT,
  otherInformation TEXT
);

-- Table to store the address of the user
CREATE TABLE address (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  houseNumber TEXT NOT NULL,
  street TEXT NOT NULL,
  town TEXT NOT NULL,
  country TEXT NOT NULL,
  zip INTEGER NOT NULL,
  branch TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Table to store information on child's parent
CREATE TABLE parent (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  mobilePhone TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  FOREIGN KEY (user_id) REFERENCES user(id)
)

-- Junction table with composite key
/* 
composite key: the combination of (parent_id, child_id) must be unique. For example (2,1) cannot be in the same table twice.
junction table: create a many-to-many relationship between entitities (one parent -> many users, one user -> many (>1, usually) parents)
*/

CREATE TABLE parent_child (
  parent_id INTEGER NOT NULL,
  child_id INTEGER NOT NULL,
  PRIMARY KEY (parent_id, child_id),
  FOREIGN KEY (parent_id) REFERENCES parent (id)
  FOREIGN KEY (child_id) REFERENCES user (id)
)