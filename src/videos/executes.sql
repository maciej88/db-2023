create table users (
    user_id uuid default gen_random_uuid() PRIMARY KEY unique,
    name text
);

create table videos(
    video_id uuid default gen_random_uuid() PRIMARY KEY unique ,
    title text,
    file_name text,
    description text,
    created timestamp default now(),
    edited timestamp default now(),
    owner uuid,
    foreign key(owner) references Users(user_id)
);
create table comments(
    comment_id uuid default gen_random_uuid() PRIMARY KEY UNIQUE,
    author_id uuid,
    content text,
    created timestamp default now(),
    edited timestamp default now(),
    foreign key(author) references Users(user_id)
);
create table videolikes(
    like_id uuid DEFAULT gen_random_uuid() PRIMARY KEY UNIQUE,
    video_id uuid UNIQUE,
    user_id uuid UNIQUE,
    like_level int CHECK (like_level in (0, -1, 1)) DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (video_id) REFERENCES videos (video_id),
    CONSTRAINT unique_vote UNIQUE (user_id, video_id)
    );