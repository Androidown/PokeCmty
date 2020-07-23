CREATE TABLE IF NOT EXISTS `PM_STATS` (
    `species` SMALLINT UNSIGNED,
    `form` TINYINT UNSIGNED DEFAULT 0,
    `HP` TINYINT UNSIGNED,
    `ATK` TINYINT UNSIGNED,
    `DEF` TINYINT UNSIGNED,
    `SPA` TINYINT UNSIGNED,
    `SPD` TINYINT UNSIGNED,
    `SPE` TINYINT UNSIGNED,
    `type1` TINYINT UNSIGNED,
    `type2` TINYINT UNSIGNED,
    `ability1` SMALLINT UNSIGNED,
    `ability2` SMALLINT UNSIGNED,
    `abilityH` SMALLINT UNSIGNED,
    `name_CHS` VARCHAR(5),

    PRIMARY KEY (`species`, `form`)
) ENGINE=Myisam DEFAULT CHARSET=utf8;



import mysql.connector as ctr
mysql_db = ctr.connect(
    host='192.168.29.30',
    user='root',
    passwd='root',
    database='POKEMON'
)
cursor = mysql_db.cursor()
sql = "insert into pkmstat_pokemon (species, form, HP, ATK, DEF, SPE, SPA, SPD, name_CHS, ability1, ability2, abilityH, type1 {}) values ({})"
for i in range(893):
    pm = PKMPersonal(i)
    if pm.HP == 0:
        continue
    for alter in range(pm.forme_count):
        pm_a = PKMPersonal(i, alter)
        if pm_a.HP == 0:
            continue
        vals = f"{i}, {alter}, {pm_a.HP}, {','.join(map(str, pm_a.STAS))}, '{SPECIES[i]}', {','.join(map(str, pm_a.abilities))}, {pm_a.type1}"
        type_key = ''
        if pm_a.type1 != pm_a.type2:
            type_key = ',type2'
            vals += f", {pm_a.type2}"
        print(sql.format(type_key, vals))
        cursor.execute(sql.format(type_key, vals))

mysql_db.commit()
mysql_db.close()
