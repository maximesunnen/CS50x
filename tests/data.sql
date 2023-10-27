-- Create a test user
INSERT INTO user (first_name, last_name, username, password, birthday, gender)
VALUES
    ("John", "Doe", "johndoe", "scrypt:32768:8:1$ZbYoAaLvUL8DtWSD$684f63fd373e37599c99cfd87a21ffe720c82419e95830f67d5cc850f6e7e064a3176b830bafe917da5d8312452718019eeb9dbc1db6586df6891fb17d7539a6", "1997-01-25", "male");