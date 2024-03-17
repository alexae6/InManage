create user dbadmin identified by 'password';
grant all on djangodatabase.*  to 'dbadmin'@'%';
flush privileges;
