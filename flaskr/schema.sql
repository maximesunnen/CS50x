DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS parent;
DROP TABLE IF EXISTS emergency;
DROP TABLE IF EXISTS parent_child_emergency;
DROP TABLE IF EXISTS data_protection;

-- Table to store user (child) information
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  number TEXT,
  email TEXT,
  birthday DATE NOT NULL,
  gender TEXT NOT NULL,
  allergies TEXT,
  diet TEXT,
  branch TEXT,
  other_information TEXT
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

-- Table storing information on child's parent
-- no UNIQUE constraints: i check if a parent alredy exists in the db in my backend
CREATE TABLE parent (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  email TEXT NOT NULL
);

-- Table storing information on child's emergency contact
-- no UNIQUE constraints: i check if an emergency contact alredy exists in the db in my backend
CREATE TABLE emergency (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  email TEXT NOT NULL
);

-- Junction table with composite key
/* 
composite key: the combination of (parent_id, child_id) must be unique. For example (2,1) cannot be in the same table twice.
junction table: create a many-to-many relationship between entitities (one parent -> many users, one user -> many (>1, usually) parents)
*/

CREATE TABLE parent_child_emergency (
  parent_id INTEGER NOT NULL,
  child_id INTEGER NOT NULL,
  emergency_id INTEGER NOT NULL,
  PRIMARY KEY (parent_id, child_id, emergency_id),
  FOREIGN KEY (parent_id) REFERENCES parent (id),
  FOREIGN KEY (child_id) REFERENCES user (id),
  FOREIGN KEY (emergency_id) REFERENCES emergency (id)
);

CREATE TABLE data_protection (
  child_id INTEGER NOT NULL,
  pictures BOOLEAN NOT NULL,
  social_media BOOLEAN NOT NULL,
  contact BOOLEAN NOT NULL,
  home_alone BOOLEAN NOT NULL,
  FOREIGN KEY (child_id) REFERENCES user (id)
)