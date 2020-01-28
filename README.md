# Tracker 
Simple Django application, aggregating favourite news.


## Supported Services

### Reddit
Tracker supports both Reddit's main page and subreddits. It automatically modify provided urls to Reddit's API urls. By providing adequate link, user can specify stories ordering. Valid urls:
- https://www.reddit.com/r/Python/
- https://www.reddit.com/r/Python/top/
- https://www.reddit.com/r/Python/top/?t=month

Urls pointing directly to Reddit's API (containing `.json`) are not valid Tracker urls.

### RSS feeds
Tracker supports 2.0 RSS feeds, although some of `<item>` subelements are required:
- **title**
- **link**
- **guid**

Optional:
- description
- author

## Aggregating news
To run scrapers (aggregate new stories) once, use following management command:
```
python manage.py runscrapers
```
Use `cron` to run the command periodically and automize the process of aggregating news.