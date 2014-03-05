INSERT INTO people(username, first_name, last_name, hash) VALUES(
  'martin',
  'Martin',
  'Rechsteiner',
  'cK5Q20EMG/x0yiANC5HcWOS7//ptQeso5cJVWf9TJKyXMrloUY'
);

INSERT INTO people(username, first_name, last_name, hash) VALUES(
  'kjersti',
  'Kjersti',
  'Fagerholt',
  'cK5Q20EMG/x0yiANC5HcWOS7//ptQeso5cJVWf9TJKyXMrloUY'
);

INSERT INTO events(description, start_time, end_time, owner) VALUES(
  'Meeting',
  '2013-10-16 00:25:17.005983',
  '2013-10-16 00:25:17.005983',
  1
);

INSERT INTO event_participants(invite_status, person_id, event_id) VALUES(
  0,
  1,
  1
);

INSERT INTO event_participants(invite_status, person_id, event_id) VALUES(
  0,
  2,
  1
);

INSERT INTO rooms(name, capacity) VALUES(
  "BU1-110",
  1
);

INSERT INTO event_rooms(room_id, event_id) VALUES(
  1,
  1
);