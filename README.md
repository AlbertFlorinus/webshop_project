Projektuppgift
--------------

Webshopen BestBuy (ingen sammankoppling till butiken med samma namn i U.S.A finns) är en försäljare för kläder. De har hitintills haft ett fungerande system där de använt sig av kommaseparerade (csv) filer för att hantera produkter, kunder, och ordrar. I dagsläget fungerar det, men de vill säkra sig för framtiden genom att uppgradera till en databas istället för detta filbaserade system.

På [http://www.student.bth.se/~frer01/databas/](http://www.student.bth.se/~frer01/databas/) återfinner ni nuvarande implementation, där ni kan se hur allting fungerar och testa göra ordrar och så vidare. Källkoden kan ni ladda ner från [gitlab.bth.se/courses/database-project](https://gitlab.bth.se/courses/database-project/tree/master) och spara i er **www** katalog på er studentserver (antingen via [FileZilla](https://dbwebb.se/kunskap/flytta-filer-till-driftsmiljon-med-sftp-och-filezilla), eller J: via [VPN](https://studentportal.bth.se/page/lagra-dokument-och-filer)). När ni laddat upp filerna www katalogen i er student-katalog (J:) kommer ni åt er webshop via [http://www.student.bth.se/~<er_akronym>/](http://www.student.bth.se/~<er_akronym>/), för att testa vidare själva och förstå hur koden fungerar (börja med att ladda upp alla filer från gitlab och se att det fungerar innan ni börjar ändra).

Alternativt kan ni köra all kod lokalt på er egen maskin och då startar ni en webbserver med kommandot: `python -m http.server --cgi 8000` (där 8000 är portnummer) sen kan ni komma åt er lokala version på http://localhost:8000 och göra ändringar lokalt.

Er uppgift är att skriva om filen [utilities.py](https://gitlab.bth.se/courses/database-project/blob/master/cgi-bin/utilities.py) så att ni, istället för att använda [Pandas](https://pandas.pydata.org/pandas-docs/stable/) och csv-filer, använder den databas ni skapat i [Modelleringsövningen till projektet](https://bth.instructure.com/courses/621/assignments/668 "Modelleringsövning till projektet"). Värt att notera, inte all data som finns specificerad i modelleringsövningen finns för nuvarande i aktuellt system.

Funktionaliteten som finns på hemsidan just nu skall ni återskapa, d.v.s funktionerna:
```python
get_products_filtered()
get_products_search()
get_products_ids()
get_categories()
get_subcategories()
write_order()
get_20_most_popular()
```

skall ni skriva om så att de använder er egenskapade databas istället för det som nuvarande finns där. Viktigt att tänka på är att indatan och utdatan från funktionerna skall vara densamma, annars kommer hemsidan inte fungera. Under rubriken Referenser finner ni dokumentation och "kom-igång-guide" för python, samt dokumentation för modulen ni skall använda som ansvarar för databaskopplingen.

I funktionen nedan ska ni plocka bort de första fyra raderna och skiva Python kod som ansluter till databasen och plockar ut **produkter filtrerat på kategori** (ni kommer alltså att kalla på era procedurer och göra SELECT från era vyer från Python som i exemplet nedan).

```python
    def get_products_filtered(categories=None):
    	df = pd.read_csv('data/Products.csv')
    	if categories is not None:
    		for category in categories.keys():
    			df = df[df[category] == categories[category]]
    	''' SQL '''

    	return df.to_dict('records')
```

Tips från oss är att ni stegvis gör den här uppdateringen av systemet, dvs. ändra inte alla funktioner till databasimplementationer utan att testa dem. Gör en i taget så att det fungerar på samma sätt som det nuvarande systemet.

I projektkatalogen på gitlab finns det en `data` katalog som innehåller produkterna som CSV-filer ni behöver inte använda denna datan.

## Ansluta till en databas via Python

Nedan finner ni en simpel exempelkod för att verifiera att ni kan ansluta till en databas, göra queries, och hämta ut data:
```python
import mysql.connector as mysql

database = mysql.connect(user='',  # STUDENT_ID
                         passwd='',  # Losenord
                         database='',  # STUDENT_ID
                         host='blu-ray.student.bth.se')
cnx = connection.cursor(dictionary=True)

c.execute('''CREATE TABLE Names (name varchar(20))''')
c.execute('''INSERT INTO Names VALUES ('test')''')
c.execute('''SELECT * FROM Names''')

for row in c:
    print("{name}".format(name=row[name]))
```

## Referenser

* [Python For Beginners](https://www.python.org/about/gettingstarted/)
* [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)
* [Python 4 Java programmers](http://python4java.necaiseweb.org/Fundamentals/TheBasics)
* [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)
