lights = {"ambient":0,
          "treestar":1,"treetop":2,"treemid":3,"treelow":4,"treebot":5,
          "phone":6,"santa":7,"skaters":8,"shops":9,"train":10,"starchange":11,"smallstar":12,              
          "lampposts":13}

startscene = [[("treestar",100,5,0),
               ("treebot",100,3,4),
               ("treelow",100,3,3),
               ("treemid",100,3,2),
               ("treetop",100,3,1),
               ("smallstar",100,2,5),
               ("santa",100,3,9),
               ("train",100,3,7),
               ("skaters",100,0,5),
               ("shops",100,5,8),
               ("lampposts",100,6,8),
               ("starchange",100,1,10),
               ("ambient", 100, 20 ,10),
               ("phone",100,3,10),
              ],
               20,
             ]
scenario1 = [[("treebot",100,3,0),
              ("treelow",100,3,1),
              ("treemid",100,3,3),
              ("treetop",100,3,4),
              ],
              10,
            ] #fade up to 100% for 10s


scenario2 = [[("treebot",2,2,6),
              ("treelow",2,3,3),
              ("treemid",2,3,2),
              ("treetop",2,3,1),
             ],
             10,
            ]

scenario3 = [[("treebot",100,1,0),
              ("treelow",100,1,3),
              ("treemid",100,1,5),
              ("treetop",100,1,7),
              ],
              8,
             ]

scenario4 = [[("treebot",1,1,0),
              ("treelow",1,1,1),
              ("treemid",1,1,2),
              ("treetop",1,1,3),
              ],
              5,
             ]


endscene = [[("ambient", 0, 7,0),
             ("santa",0,3,9),
             ("train",0,3,9),
             ("skaters",0,3,15),
             ("shops",0,10,8),
             ("lampposts",0,15,8),
             ("phone",0,3,8),
             ("treebot",0,3,15),
             ("treelow",0,3,16),
             ("treemid",0,3,17),
             ("treetop",0,3,18),
             ("starchange",0,1,12),             
             ("smallstar",0,5,13),
             ("treestar",0,7,15),
            ],
             30,
           ]


act1 = {"act1":([startscene],False)}

act2 = {"act2":([scenario1,scenario2,scenario3,scenario4],True)}

act3 = {"act3":([endscene],False)}

acts = [act1, act2 ,act3]

