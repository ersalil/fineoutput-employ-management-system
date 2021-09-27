css_active = '''QFrame{
                background-color: white;
            border-right:2px solid orange;
            }
            QPushButton{
                padding: 10px 15px;
                border: none;
                border-radius: 0px;
                background-color: orange;
                color: white;
            margin-top:0px 0px;
            font-size :17px;
            text-align:left;

            }
            QPushButton:hover{
               padding: 10px 15px;
                border: none;
                border-radius: 0px;
                background-color: orange;
                color: white;
            margin-top:0px 0px;

            text-align:left;
            font-size :18px;

            color:white;
            border:1px solid white;
            }

            QPushButton:pressed {
                    background-color:orange;
            font-size :16px;

            color:white;
            
            }

            '''

css_not_active = '''QFrame{
                background-color: white;
            border-right:2px solid orange;
            }
            QPushButton{
                padding: 10px 15px;
                border: none;
                border-radius: 0px;
                background-color: white;
                color: orange;
            margin-top:0px 0px;
            font-size :17px;
            text-align:left;

            }
            QPushButton:hover{
               padding: 10px 15px;
                border: none;
                border-radius: 0px;
                background-color: orange;
                color: white;
            margin-top:0px 0px;

            text-align:left;
            font-size :18px;

            color:white;
            border:1px solid white;
            }

            QPushButton:pressed {
                    background-color:orange;
            font-size :16px;

            color:white;
            
            }

            '''

css_qlistwidget = '''QListWidget { font: 18pt "Verdana";}
                    QListWidget::item:selected { color: white;}
                    QListWidget::item:selected { background-color: orange; }
                       
                    QListWidget:QScrollBar:vertical {              
                                border: none;
                                background:white;
                                width:3px;
                                margin: 0px 0px 0px 0px;
                            }
                    QListWidget:QScrollBar::handle:vertical {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
                                min-height: 0px;
                            }
                    QListWidget:QScrollBar::add-line:vertical {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
                                height: 0px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }
                    QListWidget:QScrollBar::sub-line:vertical {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
                                height: 0 px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                        
                    '''