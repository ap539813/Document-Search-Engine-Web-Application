show databases;
use docsearch;
show tables;

create table datastorage
	( id_source int primary key auto_increment,
    type int,
    path varchar(100));
    
show tables;

insert into datastorage
	(type, path)
    values
    (1, 'https://www.gfmer.ch/Medical_journals/Oncology.htm'),
    (2, 'http://www.cancerbiomed.org/index.php/cocr/article/viewFile/1830/1774'),
    (3, 'Data/'),
    (4, 'Data/'),
    (2, 'http://www.cancerbiomed.org/index.php/cocr/article/view/1854/1903');
    
drop table datastorage;
    
    
select * from datastorage;

insert into datastorage (type, path) values(3, "Data/1801-6137-2-PB.pdf");
select * from datastorage;


