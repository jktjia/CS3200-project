-- This file is to bootstrap a database for the CS3200 project. 

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
create database loggr;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privileges to the new database we just created.
grant all privileges on loggr.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
use loggr;

-- Put your DDL
create table if not exists enterprises (
    id int primary key not null auto_increment,
    name varchar(75) unique not null
);

create table if not exists users (
    id int primary key auto_increment,
    username varchar(50) not null,
    email varchar(75) not null,
    password varchar(50) not null,
    joined_at datetime not null default current_timestamp,
    last_active datetime not null default current_timestamp, -- not sure how to enforce this updates when they are active
    birthday datetime,
    first_name varchar(20),
    last_name varchar(20),
    enterprise_id int,
    constraint u_enterprise_fk foreign key (enterprise_id) references enterprises(id)
      on update cascade on delete restrict
);

create table if not exists categories ( -- these are forests but for my sanity they're called categories in the code
    id int primary key auto_increment,
    topic varchar(50) unique not null
);

create table if not exists user_follows_categories (
    user_id int,
    category_id int,
    primary key (user_id, category_id),
    constraint ufc_user_fk foreign key (user_id) references users(id)
      on update cascade on delete cascade,
    constraint ufc_category_fk foreign key (category_id) references categories(id)
      on update cascade on delete restrict
);

create table if not exists user_follows_users (
    follower_id int not null,
    user_id int not null,
    constraint ufu_follower_fk foreign key (follower_id) references users(id)
      on update cascade on delete cascade,
    constraint ufu_user_fk foreign key (user_id) references users(id)
      on update cascade on delete cascade
);

create table if not exists log_lists ( -- these are groves but for my sanity they're called log lists in the code
    id int primary key auto_increment,
    is_private boolean not null default true,
    name varchar(75) not null,
    description text,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp
        on update current_timestamp,
    category_id int,
    constraint ll_category_fk foreign key (category_id) references categories(id)
      on update cascade on delete restrict
);

-- table of access types granted to users for private logs
create table if not exists user_log_list_accesses (
    user_id int not null,
    log_list_id int not null,
    access varchar(10) not null,
    primary key (user_id, log_list_id),
    constraint ulla_user_fk foreign key (user_id) references users(id)
      on update cascade on delete cascade,
    constraint ulla_log_list_fk foreign key (log_list_id) references log_lists(id)
      on update cascade on delete cascade,
    constraint ll_access_types_ck check
        access = 'creator' or access = 'write' or access = 'comment' or access = 'read'
);

create table if not exists logs (
    id int primary key auto_increment,
    title tinytext not null,
    content text,
    rating int,
    log_list_id int not null,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp,
    created_by int not null,
    constraint l_log_list_fk foreign key (log_list_id) references log_lists(id)
      on update cascade on delete cascade,
    constraint l_rating_0_to_5_chk check (rating is null or (rating >= 0 and rating <= 5)),
    constraint l_user_fk foreign key (created_by) references users(id)
      on update cascade on delete cascade
);

create table if not exists comments (
    id int primary key auto_increment,
    content text not null,
    log_id int not null,
    user_id int not null,
    constraint c_log_fk foreign key (log_id) references logs(id)
      on update cascade on delete cascade,
    constraint c_user_fk foreign key (user_id) references users(id)
      on update cascade on delete cascade
);

-- public likes to signal to original creator that the user liked the log
create table if not exists user_liked_logs (
    user_id int,
    log_id int,
    liked_at datetime default current_timestamp,
    primary key (user_id, log_id),
    constraint ufl_user_fk foreign key (user_id) references users(id)
      on update cascade on delete cascade,
    constraint ufl_log_fk foreign key (log_id) references logs(id)
      on update cascade on delete cascade
);

-- privately saved logs for later reference
create table if not exists user_saved_logs (
    user_id int,
    log_id int,
    primary key (user_id, log_id),
    constraint usl_user_fk foreign key (user_id) references users(id)
      on update cascade on delete cascade,
    constraint usl_log_fk foreign key (log_id) references logs(id)
      on update cascade on delete cascade
);

create table if not exists enterprise_categories (
    enterprise_id int not null,
    category_id int not null,
    primary key (enterprise_id, category_id),
    constraint ec_enterprise_fk foreign key (enterprise_id) references enterprises(id)
      on update cascade on delete cascade,
    constraint ec_category_fk foreign key (category_id) references categories(id)
      on update cascade on delete restrict
);

create table if not exists credit_cards (
    id int primary key auto_increment, -- pseudo primary key
    number varchar(20) unique not null, -- this is a string not a number because it's better that way
    security_code int(3) not null,
    expiration datetime not null,
    first_name varchar(25) not null,
    last_name varchar(25) not null
);

-- i think this should be restructured so that credit_cards are weak entities
create table if not exists enterprise_credit_cards (
    enterprise_id int not null,
    credit_card_id int not null,
    primary key (enterprise_id, credit_card_id),
    constraint ecc_enterprise_fk foreign key (enterprise_id) references enterprises(id)
      on update cascade on delete restrict,
    constraint ecc_credit_card_fk foreign key (credit_card_id) references credit_cards(id)
      on update cascade on delete restrict
);

-- Add sample data.
/*insert into enterprises (name)
values ('Corkery-Rosenbaum'),
       ('Wunsch, Harber and Schmidt'),
       ('Gulgowski-Jenkins'),
       ('Gleason-Schiller'),
       ('Haag, Hoppe and Von');

insert into users (username, email, password, birthday, first_name, last_name, enterprise_id)
values ('pprantl0', 'pprantl0@sourceforge.net', 'oP2?0=Qid0', '1963-07-09', 'Pris', 'Prantl', 1),
       ('reringey1', 'reringey1@dion.ne.jp', 'qV9~,Y_JT>ZJjZi', '1969-03-08', 'Rosabelle', 'Eringey', 3),
       ('ajoslin2', 'ajoslin2@thetimes.co.uk', 'dQ2{G7@+!Ab*jC', '2020-07-30', 'Alanna', 'Joslin', 2),
       ('ltomlett3', 'ltomlett3@example.com', 'dR0@t79(Fk3}C*8', '2017-04-29', 'Leonerd', 'Tomlett', 2),
       ('spaulmann4', 'spaulmann4@cbslocal.com', 'aC8@)rl2#RC', '1994-04-06', 'Shaine', 'Paulmann', null),
       ('agauson5', 'agauson5@mozilla.org', 'yN7#)JH)M', '1972-02-14', 'Arda', 'Gauson', 5),
       ('nweal6', 'nweal6@sina.com.cn', 'pP3$.kE1X|1o', '1994-04-12', 'Noe', 'Weal', null),
       ('twilkerson7', 'twilkerson7@technorati.com', 'tT1+1Sr%+<M', '1994-04-12', 'Tonia', 'Wilkerson', null),
       ('kduckham8', 'kduckham8@senate.gov', 'vM3@W"@"i5a6', '1932-04-29', 'Kippar', 'Duckham', null),
       ('avaskin9', 'avaskin9@bbb.org', 'iH7%&Bd!xgYDQ}V', '2019-07-10', 'Aprilette', 'Vaskin', 4);

insert into categories (topic)
values ('music'), ('video games'), ('hiking'), ('books'), ('movies');

insert into user_follows_categories (user_id, category_id)
values (5, 5), (5, 1), (3, 2), (4, 3), (8, 2),
       (6, 4), (7, 5), (8, 5), (6, 3), (8, 3);

insert into user_follows_users (follower_id, user_id)
values (6, 2), (3, 8), (1, 3), (5, 6), (8, 2);

insert into log_lists (is_private, name, description, category_id)
values (false, 'ac nulla sed vel enim sit amet nunc', 'Phasellus sit amet erat. Nulla tempus.', 1),
       (true, 'sapien', 'Nulla justo. Aliquam quis turpis eget elit sodales scelerisque.', null),
       (false, 'quam a odio in', 'Nulla facilisi.', 4),
       (false, 'magnis', 'Nulla facilisi. Cras non velit nec nisi vulputate nonummy.', 2),
       (true, 'id massa id nisl venenatis lacinia', 'Phasellus in felis.', null),
       (false, 'mauris laoreet ut rhoncus', 'In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl.', 4),
       (true, 'odio curabitur convallis duis consequat dui nec nisi volutpat eleifend', 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus.', null),
       (true, 'mi integer ac neque duis bibendum morbi non quam', 'Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', null),
       (false, 'sem fusce consequat nulla nisl', 'Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit.', 2),
       (false, 'dui nec nisi volutpat eleifend donec ut dolor morbi vel', 'Phasellus id sapien in sapien iaculis congue.', 5);

insert into user_log_list_accesses (user_id, log_list_id, access_id)
values (9, 5, 'write'), (6, 5, 'write'), (9, 7, 'comment'), (6, 8, 'write'), (3, 5, 'write'),
       (5, 7, 'write'), (1, 7, 4), (2, 2, 'read'), (1, 8, 'comment'), (8, 2, 'read'),
       (8, 1, 'creator'), (9, 2, 'creator'), (4, 3, 'creator'), (6, 4, 'creator'), (1, 5, 'creator'),
       (10, 6, 'creator'), (6, 7, 'creator'), (10, 8, 'creator'), (6, 9, 'creator'), (4, 10, 'creator');

insert into logs (title, content, log_list_id, created_by)
values ('et ultrices posuere cubilia curae mauris', 'Proin risus. Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus. Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis.', 1, 8),
       ('erat tortor sollicitudin mi sit amet lobortis', 'Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla. Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam. Nam tristique tortor eu pede.', 6, 10),
       ('et ultrices posuere cubilia curae nulla', 'Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 8, 10),
       ('massa donec dapibus', 'Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus. Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis.', 4, 6),
       ('in hac habitasse', null, 1, 8);

insert into logs (title, content, rating, log_list_id, created_by)
values ('varius integer ac leo pellentesque ultrices', 'Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem. Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue.', 4, 8, 10),
       ('eu magna vulputate luctus cum sociis natoque penatibus et magnis', 'Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque.', 5, 10, 4),
       ('ullamcorper augue a', 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus.', 3, 8, 10),
       ('at nibh in hac', 'Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue.', 4, 2, 9),
       ('pulvinar nulla pede ullamcorper augue a', null, 5, 1, 8);

insert into comments (content, log_list_id, user_id)
values  ('Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 8, 1),
        ('Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor. Duis mattis egestas metus. Aenean fermentum.', 4, 2),
        ('Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis.', 6, 3),
        ('Phasellus in felis. Donec semper sapien a libero. Nam dui. Proin leo odio, porttitor id, consequat in, consequat ut, nulla.', 5, 4),
        ('In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst.', 5, 5);

insert into user_liked_logs (user_id, log_id)
values (10, 6), (8, 5), (9, 7), (9, 5), (6, 3);

insert into user_saved_logs (user_id, log_id)
values (6, 10), (5, 8), (7, 9), (5, 9), (6, 3);

insert into enterprise_categories (enterprise_id, category_id)
values (1, 5), (2, 5), (3, 3), (4, 5), (5, 1),
       (5, 2), (3, 5), (3, 4), (5, 4), (3, 2);

insert into credit_cards (number, security_code, expiration, first_name, last_name)
values ('5367372710060939', 042, '2023-07-01', 'Antony', 'Muzzullo'),
       ('5602238967949584', 035, '2023-01-01', 'Adriano', 'Thomelin'),
       ('630481727686778887', 116, '2023-03-01', 'Wini', 'Norrey'),
       ('50187783843821118', 978, '2023-09-01', 'Juliane', 'Stennes'),
       ('5602211023686060', 625, '2023-08-01', 'Deva', 'Stilgoe'),
       ('3589776030315343', 352, '2023-08-01', 'Noak','Kersley'),
       ('633110297704594529', 047, '2023-10-01', 'Daniele', 'Franceschi'),
       ('3544634530104390', 055, '2023-06-01', 'Christan', 'Hounsome');

insert into enterprise_credit_cards (enterprise_id, credit_card_id)
values (1,1), (2,2), (3,4), (4,5), (5,3),
       (4,6), (2,7), (2,8);*/