
create table users
(
    uid  uuid default gen_random_uuid() primary key,
    name text not null
);

create table elections
(
    eid uuid default gen_random_uuid() primary key,
    name text not null
);

create table participation(
    eid uuid not null references elections on delete cascade ,
    uid uuid not null references users on delete cascade
);

create table tokens(
    eid uuid not null references elections on delete cascade ,
    tokenid uuid default gen_random_uuid() primary key
);

create table votes(
    eid uuid not null references elections on delete cascade,
    votevalue int not null
);

drop table participation;
drop table votes;
drop table tokens;
drop table elections;
drop table users;

