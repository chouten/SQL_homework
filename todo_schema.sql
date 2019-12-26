create table spendings (
    category    text primary key,
    amount      integer,
    timedate    date
);


create table subcategory (
    id           integer primary key autoincrement not null,
    amount_spent integer,
    details      text,
    when_spent   date,
    category     text not null references spendings(category)
);

