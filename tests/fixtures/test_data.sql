INSERT INTO card (id, name, setname, count, img)
VALUES
(1,"Mother of Runes","ulg",1,"https://c1.scryfall.com/file/scryfall-cards/normal/front/0/b/0b1a46ab-95cb-4c24-924f-fc2afd4fcac7.jpg?1562862312"),
(2,"Adanto Vanguard","xln",1,"https://c1.scryfall.com/file/scryfall-cards/normal/front/2/1/21c950d7-b4f6-4902-8c9a-98f2933f9fa5.jpg?1562552020"),
(3,"Fencing Ace","ddl",1,"https://c1.scryfall.com/file/scryfall-cards/normal/front/1/7/170240bb-73a7-4a22-aedc-4e2323299a4d.jpg?1592751748");

INSERT INTO price (id, price, card_id, date)
VALUES
(1,0.05,1, "2021-05-30 07:41:30.818387"),
(2,0.1,1,"2021-05-31 07:41:30.818387"),
(3,0.16,2,"2021-05-30 07:41:30.818387"),
(4,4.99,2,"2021-05-31 07:41:30.818387"),
(5,0.35,3,"2021-05-30 07:41:30.818387"),
(6,0.13,3,"2021-05-31 07:41:30.818387");

INSERT INTO collection (id, name)
VALUES
(1,"Collection 1"),
(2,"Collection 2");

INSERT INTO collection_card_rel (collection_id, card_id)
VALUES
(1,1),
(1,2),
(2,1),
(2,3);