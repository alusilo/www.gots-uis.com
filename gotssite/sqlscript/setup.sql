drop database gotssite;
drop user gotssite_user;
create database gotssite;
create user gotssite_user with encrypted password '123456';
grant all privileges on database gotssite to gotssite_user;