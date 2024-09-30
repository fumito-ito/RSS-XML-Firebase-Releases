# RSS XML for Firebase Releases

**This is unofficial RSS feed for firebase releases**

[Firebase releases page](https://firebase.google.com/support/releases) provides a changelog that lists new SDK releases and describes updates to the Firebase console and Firebase services. But this page does not have any RSS feed.

`generate_rss.py` fetches release page and generates rss items. This script is executed once a day via cron.
Generated XML is surved by [GitHub Pages](https://fumito-ito.github.io/RSS-XML-Firebase-Releases/firebase_releases.xml). Feel free to use it. 

## Contributing

Pull requests are welcome. Do you have any Issues ? please open an issue first to discuss what you encounter.