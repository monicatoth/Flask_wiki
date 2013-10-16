drop table if exists pages;
create table pages (
	id integer primary key autoincrement,
	created timestamp default (strftime('%s', 'now')),
	last_updated timestamp default (strftime('%s', 'now')),
	title text not null,
	content text not null
);

create table pages_to_tags (
	id integer primary key autoincrement,
	created timestamp default (strftime('%s', 'now')),
	page_id integer not null,
	tag_id integer not null
);

create table tags (
	id integer primary key autoincrement,
	created timestamp default (strftime('%s', 'now')),
	tag text not null
);