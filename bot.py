import os
import random
import discord
import sqlite3

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.command(name='poro', help='Habla con Poro :)')
async def poro(ctx):
    poro_quotes = [
        'Tengo hambre...',
        'Grrrr!',
        (
            'Es hora de League of Legends! '
            "Let's go"
        ),
        'Dame amor <3',
        'Cookies!',
        ':3'
    ]

    response = random.choice(poro_quotes)
    await ctx.send(response)


@bot.command(name='decide', help='Poro decide por ti.')
async def decide(ctx, *options: str):
    decision = options[random.choice(range(0, len(options)))]
    await ctx.send("Poro ha decidido que lo mejor es: " + decision)


@bot.command(name='add', help='Añade a un jugador de League of Legends a la lista')
async def add(ctx, player: str):

    # Comprueba si el jugador ya existe en la lista
    found = False
    with open("jugadores.txt") as fichero:
        for linea in fichero:
            linea = linea.rstrip()  # quita '\n' al final de la línea
            if player == linea:
                found = True
                break

    if(found):
        await ctx.send("El jugador " + player + " ya está en la lista de jugadores.")
    else:
        # Añade al player al fichero jugadores.txt  
        f = open("jugadores.txt", "a")
        f.write(player + '\n')
        f.close()
        await ctx.send("Se ha añadido a " + player + " a la lista de jugadores.")


@bot.command(name='del', help='Elimina a un jugador de League of Legends de la lista')
async def delete(ctx, player: str):
    # Cada línea acaba con el caracter '\n', para hacer que la comparación sea correcta añadimos este caracter a la búsqueda
    player += '\n'

    found = False
    with open("jugadores.txt", "r+") as fichero:
        lineas = fichero.readlines()
        fichero.seek(0)
        for linea in lineas:
            if linea != player:
                fichero.write(linea)
            else:
                found = True
        fichero.truncate()

    player = player.rstrip() # quita '\n' al final de la línea
    if(found):
        await ctx.send("El jugador " + player + " se ha eliminado la lista de jugadores")
    else:
        await ctx.send("El jugador " + player + " no se encuentra en la lista de jugadores")


@bot.command(name='list', help='Muestra los jugadores añadidos a la lista de League of Legends')
async def list(ctx):
    players = ""
    with open("jugadores.txt") as archivo:
        for player in archivo:
            players += " - " + player
    await ctx.send("Lista de jugadores añadidos:\n" + players)

@bot.command(name='cookie', help='Alimenta al poro con una cookie')
async def cookie(ctx):
    # Nombre del donante
    donor = str(ctx.author.name)

    poro_quotes = [
        'Ñam, ñam, Ñam',
        'Quiero más',
        'Gracias :3',
        '¿Solo una?',
        'Gracias por la cookie!',
        'Rico, rico',
        'A poro le gustan las cookies :)',
        'Poro ama a '+ donor + ' :3'
    ]
    response = random.choice(poro_quotes)

    await ctx.send(donor + " ha dado una cookie al poro. " + response)

    try:
        # Connexión con la BBDD
        sqliteConnection = sqlite3.connect('Poro.db')
        cursor = sqliteConnection.cursor()
        print("Database connectada con éxito")

        # Comprueba si el Donor ya ha dado cookies anteriormente
        query = "SELECT * from cookies WHERE donor = ?"
        values = (donor)
        cursor.execute(query, (values,))
        records = cursor.fetchall()
        
        
        if(records):
            # Si ya ha dado anteriormente datos, sumamos una cookie a las cookies donadas
            query = "UPDATE cookies SET quantity = quantity + 1"
            cursor.execute(query)
            sqliteConnection.commit()
        else:
            # Si no ha dado cookies anteriormente, se añade por primera vez y se le pone valor 1
            print("No hay datos")
            query = "INSERT INTO cookies (donor, quantity) VALUES (?, ?);"
            values = (donor, 1)
            cursor.execute(query, values)
            sqliteConnection.commit()

        query = "SELECT sum(Quantity) from cookies"
        cursor.execute(query)
        records = cursor.fetchall()
        
        # Cantidad total de cookies comidas.
        quantity = records[0][0]

        print("Insert con éxito")
        cursor.close()
    
    except sqlite3.Error as error:
        print("Fallo al insertar datos a la tabla sqlite")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("La connexión SQLite ha sido cerrada.")

    await ctx.send("Poro ha comido " + str(quantity) + " cookies hasta el momento. Gracias por tu aportación.")


@bot.command(name='donantes', help='Muestra la lista de donantes de cookies')
async def cookie(ctx):
    try:
        # Connexión con la BBDD
        sqliteConnection = sqlite3.connect('Poro.db')
        cursor = sqliteConnection.cursor()
        
        query = "SELECT * from cookies ORDER BY quantity DESC"
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            donacion = str(row[0]) + " ha donado " + str(row[1]) + " cookies."
            await ctx.send(donacion)
        cursor.close()
    except sqlite3.Error as error:
        print("Fallo al insertar datos a la tabla sqlite")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("La connexión SQLite ha sido cerrada.")

bot.run(TOKEN)