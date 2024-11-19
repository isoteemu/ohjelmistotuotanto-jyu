
### 2. Kirjautumisen testit

Hae [kurssirepositorion]({{site.python_exercise_repo_url}}) hakemistossa _osa3/login-robot_ oleva projekti.

- Kopioi projekti palatusrepositorioosi, hakemiston _osa3_ sisälle.

Tutustu ohjelman rakenteeseen. Sovellus noudattaa ns. kerrosarkkitehtuuria. Sovelluksen käyttöliittymä on toteutettu luokkaan `App`, ja sovelluslogiikka luokkaan `UserService`.
Eräs huomionarvoinen seikka on se, että `UserService`-olio ei tallenna suoraan `User`-oliota vaan epäsuorasti `UserRepository`-luokan olion kautta. Mistä on kysymys?

Sovelluksen käyttämään tietoon kohdistuvien operaatioiden abstrahointiin sovelluslogiikasta löytyy useita _suunnittelumalleja_, kuten [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object), [Active Record](https://en.wikipedia.org/wiki/Active_record_pattern) ja [Repository](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design). Kaikkien näiden suunnittelumallien perimmäinen idea on siinä, että sovelluslogiikalta tulee piilottaa tietoon kohdistuvien operaatioiden yksityiskohdat.

Esimerkiksi repositorio-suunnittelumallissa tämä tarkoittaa sitä, että tietokohteeseen kohdistetaan operaatioita erilaisten funktioiden tai metodien kautta, kuten `find_all`, `create` ja `delete`. Tämän abstraktion avulla sovelluslogiikka ei ole tietoinen operaatioiden yksityiskohdista, jolloin esimerkiksi tallennustapaa voidaan helposti muuttaa.

Sovellukseen on määritelty repositorio-suunnittelumallin mukainen luokka `UserRepository`. Luokka tallentaa sovelluksen käyttäjiä muistiin. Jos päättäisimme tallentaa käyttäjät esimerkiksi SQLite-tietokantaan, ei tämä vaatisi muutoksia luokan ulkopuolelle.

**Asenna projektin riippuvuudet ja kokeile suorittaa `index.py`-tiedosto.** Ohjelman tuntemat komennot ovat _login_ ja _new_.

**Suorita myös projektiin siihen liittyvät Robot Framework -testit** virtuaaliympäristössä komennolla `robot src/tests`.

Tutki miten Robot Framework -testit on toteutettu hakemistossa _src/tests_. Tutki myös, miten avainsanat on määritelty _src_-hakemiston _AppLibrary.py_-tiedoston `AppLibrary`-luokassa. Huomioi erityisesti, miten testit käyttävät testaamisen mahdollistavaa `StubIO`-oliota käyttäjän syötteen ja ohjelman tulosteen käsittelyyn. Periaate on täsmälleen sama kuin viikon 1 tehtävien [riippuvuuksien injektointiin](/riippuvuuksien_injektointi/) liittyvässä esimerkissä.

Saatat löytää _.robot_-tiedostoista ennestään tuntemattomia ominaisuuksia. _resource.robot_-tiedossa on määritelty avainsana `Input Credentials`, jolla on argumentit `username` ja `password`:

```
Input Credentials
    [Arguments]  ${username}  ${password}
    Input  ${username}
    Input  ${password}
    Run Application
```

Kyseinen avainsana on käytössä _login.robot_-tiedostossa seuraavasti:

```
Input Credentials  kalle  kalle123
```

Lisäksi _login.robot_-tiedoston `*** Settings ***`-osiossa on uusi asetus, `Test Setup`. Kyseisen asetuksen avulla voimme määritellä avainsanan, joka suoritetaan _ennen jokaista testitapausta_. Tässä tapauksessa ennen jokaista testiä halutaan suorittaa avainsana `Create User And Input Login Command`, joka luo uuden käyttäjän ja antaa sovellukselle _login_-komennon.

[Täällä](/viikko3-t2) on vielä avattu hieman lisää testien toimintaperiaatetta.


**Toteuta** user storylle _User can log in with valid username/password-combination_ seuraavat testitapaukset _login.robot_-tiedostoon:

```
*** Test Cases ***
Login With Incorrect Password
# ...

Login With Nonexistent Username
# ...
```

Suorita testitapauksissa sopivat avainsanat, jotta haluttu tapaus tulee testattua.


### 3. Uuden käyttäjän rekisteröitymisen testit

Lisää testihakemistoon uusi testitiedosto _register.robot_. Toteuta tiedostoon user storylle _A new user account can be created if a proper unused username and a proper password are given_ seuraavat testitapaukset:

```
*** Test Cases ***
Register With Valid Username And Password
# ...

Register With Already Taken Username And Valid Password
# ...

Register With Too Short Username And Valid Password
# ...

Register With Enough Long But Invalid Username And Valid Password
# ...

Register With Valid Username And Too Short Password
# ...

Register With Valid Username And Long Enough Password Containing Only Letters
# ...
```

- Käyttäjätunnuksen on oltava merkeistä a-z koostuva vähintään 3 merkin pituinen merkkijono, joka ei ole vielä käytössä. Vinkki: [säännölliset lausekkeet](https://www.tutorialspoint.com/python/python_reg_expressions.htm) ja <a href="https://regexr.com/5fslc">^[a-z]+$</a>.
- Salasanan on oltava pituudeltaan vähintään 8 merkkiä ja se _ei saa_ koostua pelkästään kirjaimista.
- Säännöllisten lausekkeiden kokeilu ja testaaminen onnistuu hyvin esim. seuraavassa palvelussa <https://rubular.com/>

Säännöllisissä lausekkeissa voi hyödyntää Pythonin _re_-moduulia seuraavasti:

```python
import re

if re.match("^[a-z]+$", "kalle"):
  print("Ok")
else:
  print("Virheellinen")
```

**Tee testitapauksista suoritettavia ja täydennä ohjelmaa siten että testit menevät läpi**. Oikea paikka koodiin tuleville muutoksille on <i>src/services/user_service.py</i>-tiedoston `UserService`-luokan metodi `validate`.

**Vinkki 2**: et välttämättä tarvitse säännöllisiä lausekkeita mihinkään...

**HUOM 1:** Testitapaukset kannattaa toteuttaa yksi kerrallaan, laittaen samalla vastaava ominaisuus ohjelmasta kuntoon. Eli **ÄLÄ** copypastea ylläolevaa kerrallaan tiedostoon, vaan etene pienin askelin. Jos yksi testitapaus ei mene läpi, älä aloita uuden tekemistä ennen kuin kaikki ongelmat on selvitetty. Seuraava luku antaa muutaman vihjeen testien debuggaamiseen.

**HUOM 2:** Saattaa olla hyödyllistä toteuttaa _resource.robot_-tiedostoon avainsana `Input New Command` ja _register.robot_-tiedostoon avainsana `Input New Command And Create User`, joka antaa sovellukselle _new_-komennon ja luo käyttäjän testejä varten. Avainsana kannattaa suorittaa ennen jokaista testitapausta hyödyntämällä `Test Setup`-asetusta.

### Robot Framework -testien debuggaaminen

On todennäköistä että testien tekemisen aikana tulee ongelmia, joiden selvittäminen ei ole triviaalia. Epäonnistuneen testitapauksen kohdalla kannattaa miettiä mahdollisia syitä:

- Onko vika testissä, eli toimiiko sovellus kuten pitääkin? Voit esimerkiksi testata sovelluksen toimivuuden manuaalisesti. Jos näin on, keskity testin korjaamiseen
- Onko vika sovelluksessa, eli eikö manuaalisesti testattu sovellus toimi kuten pitäisi? Jos näin on, keskity tarkastelemaan ohjelman suoritusta epäonnistuneessa testitapauksessa

Tutustutaan seuraavaksi tekniikoihin, jotka helpottavat ja nopeuttavat virheiden metsästystä.

#### Suoritettavien testien lukumäärän rajoittaminen

Kun kohtaat epäonnistuvan testitapauksen, kannattaa testien suorittamista nopeuttaa suorittamalla vain epäonnistunut testitapaus. Jos testitapaus `Login With Correct Credentials`, voimme suorittaa ainoastaan sen seuraavalla komennolla:

```
robot -t "Login With Correct Credentials" src/tests/login.robot
```

Komennolle `robot` annetaan siis `-t`-optionin kautta suoritettavan testitapauksen nimi ja tiedosto, jossa testitapaus sijaitsee.

#### Ohjelman suorituksen seuraaminen

Jos virheen löytäminen pelkän manuaalisen testauksen avulla ei tuota tulosta, kannattaa alkaa tutkimaan miten ohjelman suoritus etenee. Ensin on jollain tavalla rajattava, missä ongelma saattaisi olla. Jos esimerkiksi `Login With Correct Credentials`-testitapaus epäonnistuu, on ongelma luultavasti `UserService`-luokan metodissa `check_credentials`. Voimme pysäyttää ohjelman suorituksen halutulle riville hyödyntämällä [pdb](https://docs.python.org/3/library/pdb.html)-moduulia:

```python
# ...
# debugattavaan tiedostoon tulee tuoda tarvittavat moduulit
import sys, pdb

class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def check_credentials(self, username, password):
        # pysäytetään ohjelman suoritus tälle riville
        pdb.Pdb(stdout=sys.__stdout__).set_trace()

        if not username or not password:
            raise UserInputError("Username and password are required")

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise AuthenticationError("Invalid username or password")

        return user

    # ...
```

Ohjelman suorituksen pysäyttäminen onnistuu siis kutsumalla `Pdb`-luokan metodia `set_trace`. Jotta tulosteet tulisivat näkyviin testien suorituksen aikana, tulee luokan konstruktorin `stdout` argumentin arvoksi asettaa `sys.__stdout__`. Tätä varten debugattavaan tiedostoon tulee tuoda `pdb`-moduulin lisäksi `sys`-moduuli, joka tapahtuu esimerkissä `import sys, pdb`-rivillä.

Käynnistä nyt ohjelma uudelleen, jotta muutokset koodiin astuvat voimaan. Suorita sen jälkeen pelkästään `Login With Correct Credentials`-testitapaus edellä mainitun ohjeen mukaisesti. Kun testitapauksen suoritus saavuttaa `check_credentials`-metodin kutsun, koodin suoritus pysähtyy ja palvelinta suorittavalle komentoriville ilmestyy seuraavanlainen komentorivi:

```
-> if not username or not password:
(Pdb)
```

Kyseessä on interaktiivinen komentorivi, jossa voimme suorittaa koodia. Nuoli (`->`) viittaa seuraavaksi suoritettavaan koodiriivin. Katsotaan komentorivin avulla, mitkä ovat muuttujien `username` ja `password` arvot:

```
(Pdb) username
'kalle'
(Pdb) password
'kalle123'
(Pdb)
```

Annamme siis komentoriville syötteen ja painamme Enter-painiketta. Jatketaan koodin suorittamista antamalla syöte `next()`. Koodi on ohittanut `if`-lauseen (koska muuttujilla oli arvot) ja on seuraavaksi suorittamassa riviä `user = self._user_repository.find_by_username(username)`:

```
-> user = self._user_repository.find_by_username(username)
(Pdb)
```

Suoritetaan rivi syöttämällä uudestaan `next()` ja tulostetaan `user`-muuttujan arvo:

```
-> if not user or user.password != password:
(Pdb) user
<entities.user.User object at 0x10f7a55e0>
```

Kun olet lopettanut debuggaamiseen, syötä `exit()` ja poista koodista `set_trace`-metodin kutsu.

### Tehtävien palauttaminen

Pushaa kaikki tekemäsi tehtävät ja GitHubiin palautusrepositorioosi ja merkkaa tekemäsi tehtävät [Timiin](https://tim.jyu.fi/view/kurssit/tie/teka3003/ohjelmistotuotanto-s2024/tehtavat/konfigurointitehtavat-osa-3)
