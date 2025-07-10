INSERT INTO comments (comment_uuid, post_uuid, timestamp, content) VALUES
('4f4b5b74-4b4f-4f3b-9c7d-79a08b4a1a10', 'b41c5fc6-9d6d-4e3a-8a3f-e624edbe1d61', UNIX_TIMESTAMP(), 'Great article! Thanks for sharing.'),
('6f8b7d62-9a3b-4f91-8f77-c9fdd024d6d9', 'b41c5fc6-9d6d-4e3a-8a3f-e624edbe1d61', UNIX_TIMESTAMP(), 'I have a question about this part.'),
('a1b2c3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d', '3e8c40ff-0204-47fd-b2fc-3cc5c7ea6aa0', UNIX_TIMESTAMP(), 'Very insightful!'),
('2a3b4c5d-6e7f-8a9b-0c1d-2e3f4a5b6c7d', '2348711f-2cbe-4f66-b39e-4763f105b011', UNIX_TIMESTAMP(), 'This helped me a lot, thank you!'),
('9a8b7c6d-5e4f-3d2c-1b0a-9f8e7d6c5b4a', '87a9bc89-91cc-45fc-b405-c41e2c9c1217', UNIX_TIMESTAMP(), 'Can you provide more examples?'),
('beefcafe-1234-5678-abcd-ef0123456789', '7fdd46db-0611-4936-b6a7-519a196be875', UNIX_TIMESTAMP(), 'Interesting approach, I like it.'),
('deadbeef-8765-4321-abcd-1234567890ab', 'e931c014-4c14-4392-968b-caaecf09f0fd', UNIX_TIMESTAMP(), 'Could be improved in some parts.'),
('f00dbabe-1122-3344-5566-778899aabbcc', 'e931c014-4c14-4392-968b-caaecf09f0fd', UNIX_TIMESTAMP(), 'Totally agree with your point.'),
('12345678-abcd-ef12-3456-abcdef123456', 'e931c014-4c14-4392-968b-caaecf09f0fd', UNIX_TIMESTAMP(), 'Looking forward to your next post.'),
('abcdef12-3456-7890-abcd-1234567890ab', '3e8c40ff-0204-47fd-b2fc-3cc5c7ea6aa0', UNIX_TIMESTAMP(), 'Saved this for future reference.');


INSERT INTO posts (post_uuid, user_uuid, timestamp, content) VALUES
('b41c5fc6-9d6d-4e3a-8a3f-e624edbe1d61', 'f1039ef5-77b9-4498-9d5e-2d8b1c26a5ff', UNIX_TIMESTAMP(), 'This is my first post.'),
('3e8c40ff-0204-47fd-b2fc-3cc5c7ea6aa0', 'f1039ef5-77b9-4498-9d5e-2d8b1c26a5ff', UNIX_TIMESTAMP(), 'Follow-up on the previous topic.'),
('2348711f-2cbe-4f66-b39e-4763f105b011', 'c5b75fa7-141c-4b3f-a621-e88730ab8cc1', UNIX_TIMESTAMP(), 'New tutorial released today!'),
('87a9bc89-91cc-45fc-b405-c41e2c9c1217', '25de7466-fb17-4e0f-a3cb-cd3f5c5a8e6a', UNIX_TIMESTAMP(), 'Let me know your thoughts on this.'),
('7fdd46db-0611-4936-b6a7-519a196be875', '3b4817cb-d83b-4df4-9c3e-6fc227e0fd8b', UNIX_TIMESTAMP(), 'Some technical notes from my project.'),
('e931c014-4c14-4392-968b-caaecf09f0fd', 'bdf8d2d3-2fd2-46c6-8bcb-3e8d0b2b5274', UNIX_TIMESTAMP(), 'Open discussion about clean architecture.');


INSERT INTO users (user_uuid, nickname, birthday) VALUES
('f1039ef5-77b9-4498-9d5e-2d8b1c26a5ff', 'n3tdo0r', '1999-11-10'),
('c5b75fa7-141c-4b3f-a621-e88730ab8cc1', 'montaoo', '2000-03-25'),
('25de7466-fb17-4e0f-a3cb-cd3f5c5a8e6a', 'menoz', '2000-11-10'),
('3b4817cb-d83b-4df4-9c3e-6fc227e0fd8b', 'mc-cat-tty', '2002-07-3'),
('bdf8d2d3-2fd2-46c6-8bcb-3e8d0b2b5274', 'tommygay', '2000-06-14')