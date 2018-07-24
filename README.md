## Welcome to MyDiary app
[![Build Status](https://travis-ci.org/j0flintking02/MyDiary.svg?branch=api)](https://travis-ci.org/j0flintking02/MyDiary) ![GitHub package version](https://img.shields.io/github/package-json/v/badges/shields.svg)

these are the routes that are availabe
- getAllEntries
    
    `api/v1/entries`
    ```javaScript
        {   
            'entry_id': '1',
            'title': 'Alice in wonder land',
            'description': 'lorem ipsun'
        },
        {   
            'entry_id': '2',
            'title': 'Alice in wonder land',
            'description': 'lorem ipsun'
        },
        {   
            'entry_id': '3',
            'title': 'Alice in wonder land',
            'description': 'lorem ipsun'
        },
        {   
            'entry_id': '4',
            'title': 'Alice in wonder land',
            'description': 'lorem ipsun'
        }

    ```

- get a single entry
    
    `api/v1/entries/1`

    ```javaScript
        {   
            'entry_id': '1',
            'title': 'Alice in wonder land',
            'description': 'lorem ipsun'
        }```

- adding an item
    
    `api/v1/entries`

    ```javaScript
        {   
            'entry_id': '1',
            'title': 'Alice in wonder land',
            'description': 'lorem ipsun'
        }
    ```
You can use the [index page](https://j0flintking02.github.io/MyDiary/) to  preview the content for your website.