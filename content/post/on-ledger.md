+++
title = "on ledger"
draft = false
date = "2017-02-23T22:30:00-03:00"
slug = "on-ledger"

+++

Llega un punto en el que hay ponerse serio con la plata. 

No es necesariamente porque te falte, pero porque sientes que podrías gastar mejor la que tienes, o estás pensando en un proyecto y un poco más de orden con los gastos es justo lo que necesitas.
Llevar un presupuesto no te vendría mal, es solo cuestión de... llevarlo.

¿Cierto?

La respuesta obvia para quienes están acostumbrados a trabajar con un computador, es una planilla de cálculo. [Microsoft Excel](https://products.office.com/es-cl/excel), [Google Spreadsheet](https://www.google.com/intl/es/sheets/about/), [Apple Numbers](http://www.apple.com/cl/numbers/), o incluso [LibreOffice Calc](https://es.libreoffice.org/descubre/calc/). El problema que tienen es que las planillas de calculo son demasiado genéricas para llevar finanzas, y hay que amoldarlas a lo que uno quiere. Cuando no se tiene claro que es lo que se quiere, esto puede terminar complicando la vida. Eso fué lo que me pasó a mi y terminé peleando con el excel más de lo que valía la pena.

Además, después de un tiempo de registrar y registrar ingresos y gastos, la planilla se vuelve un poco dificil de manejar.

Otra opción es [GNUCash](https://es.wikipedia.org/wiki/GnuCash). GnuCash, por si no lo conocen, es un software para manejo de finanzas. Está pensado para finanzas personales, y también para manejar empresas pequeñas. Pero la verdad nunca me acostumbré. Puede ser porque era la primera vez que me encontré con el [registro de partida doble](https://es.wikipedia.org/wiki/Partida_doble), o talvez la interfaz de usuario, que no era, en ese tiempo, de lo más agraciada.

Otro problema que tenía con la planilla, y en menor medida con el archivo de GNUCash, era que *el registro* vivía en una sóla parte. Claro, ahora con Dropbox, Google Drive, Onedrive o similares, es más simple, pero no siempre fué facil mantener una copia definitiva de los archivos que fuese sencillo editar en todas partes. Menos si usas Windows en el trabajo, y Linux en la casa.

Por el trabajo, estoy acostumbrado a vivir en la Linea de Comando, y por casualidad me topé con [Ledger](http://www.ledger-cli.org/), y como estaba aún experimentando con "soluciones" a mi problema, me dí el trabajo de pasar un poco de la información que ya tenía al formato de Ledger y probarlo.

##### `Ledger`... en serio?

Primero lo primero: Ledger no es para cualquiera, es una solución complicada para un problema que se puede complicar (pero no tiene que serlo).

En simple, es una herramienta para hacer calculos en un [registro de partida doble](https://es.wikipedia.org/wiki/Partida_doble).

Un registro de partida doble es un registro de contabilidad, que se usa para registrar el flujo de dinero. Esto es, de donde se obtiene, y en qué se gasta.

`Ledger` define un formato, pero no se encarga de la modificación del registro. Está pensado para que la modificación de el registro se realice con otras herramientas, siendo la más simple un mero editor de texto.

En este registro, se anota la información mínimas para poder seguir la transaccion:

* Fecha
* Receptor del Pago
* Cuenta de Origen del dinero
* Cuenta de Destino del dinero

...algo de la forma:
``` 
$ cat file.ledger
2017-02-20 Detinatario
  Cuenta de Destino  $1000
  Cuenta de Origen  -$1000
```

Con esta información, en el formato que `ledger` espera, podemos saber cuanto dinero hay en cada cuenta (el _balance_):
``` 
$ ledger -f file.ledger balance
               $1000  Cuenta de Destino
              $-1000  Cuenta de Origen
--------------------
                   0
```

Agregando un poco más de información, para poder ver realmente que es lo que está pasando:
``` 
$ cat file.ledger
2017-02-20 Destinatario
  Cuenta de Destino  $1000
  Cuenta de Origen  -$1000

2017-02-21 Destinatario 2
  Cuenta de Destino 2  $500
  Cuenta de Origen    -$500

2017-02-22 Destinatario 3
  Cuenta de Destino 3  $1200
  Cuenta de Origen    -$1200
```

podemos sacar un resumen de cuanta plata hay en cada cuenta:
``` 
$ ledger -f file.ledger balance
               $1000  Cuenta de Destino
                $500  Cuenta de Destino 2
               $1200  Cuenta de Destino 3
              $-2700  Cuenta de Origen
--------------------
                   0
```

o un registro de todas las transacciones que involucran a la cuenta de destino, incluyendo el valor que se movió en cada transaccion y, en cada registro, un total del dinero que se ha movido hasta ese momento:

``` 
$ ledger -f file.ledger register "Cuenta de Origen"
17-Feb-20 Destinatario          Cuenta de Origen             $-1000       $-1000
17-Feb-21 Destinatario 2        Cuenta de Origen              $-500       $-1500
17-Feb-22 Destinatario 3        Cuenta de Origen             $-1200       $-2700
```

simple, ¿cierto?... 

¿cierto?

¿alguien?

Parte del "problema" de `ledger` es que es muy permisivo. Cualquier cosa puede ser una `cuenta`, y cualquier número puede ser una monede (si, `ledger` permite manejar diferentes monedas). Entonces es muy facil hacer las cosas muy complicadas, mucho más complicadas de lo necesario.

El "antidoto" para esto es tomar prestadas convesiones desde el mundo de la contabilidad financiera.

Lo usual es tener 5 cuentas "padres", que ayudan a mantener el orden en el Flujo de dinero.

* **Ingresos (Income):** Cuentas donde ingresa el dinero.
* **Activos (Assets):** Cuentas que tienen los recursos, generalmente dinero.
* **Gastos (Expenses):** Cuentas para el registro de Gastos
* **Pasivos (Liabilities):** Cuentas para deudas.
* **Capital (Equity):** Cuentas para mantener el Capital. Normalmente se usa para "comenzar" el registro, indicando el estatus inicial de las finanzas.

Ojo, todo esto es convención, por lo que los nombres que se usan son al gusto del consumidor.

Junto con esto, `ledger` permite utilizar *cuentas anidadas* para guardar más detalle en los registros.
Además, como cada registro debe sumar cero, `ledger` permite dejar fuera del registro uno de los valores.

Con todo esto, podemos dejar ordenado el registro anterior. Además, aprovechamos de cambiarle los nombres a las cuentas para que tengan un poco más de sentido:

``` 
$ cat file.ledger
2017-02-20 Enel
  Gastos:Cuentas:Luz  $1000
  Activos:Cuenta Corriente

2017-02-21 Aguas Andinas
  Gastos:Cuentas:Agua  $500
  Activos:Cuenta Corriente

2017-02-22 Metrogas
  Gastos:Cuentas:Gas  $1200
  Activos:Cuenta Corriente
```

el balance queda:
``` 
$ ledger -f file.ledger balance
              $-2700  Activos:Cuenta Corriente
               $2700  Gastos:Cuentas
                $500    Agua
               $1200    Gas
               $1000    Luz
--------------------
                   0
```

y el registro de los gastos:
``` 
$ ledger -f file.ledger register Gastos
17-Feb-20 Enel                  Gastos:Cuentas:Luz            $1000        $1000
17-Feb-21 Aguas Andinas         Gastos:Cuentas:Agua            $500        $1500
17-Feb-22 Metrogas              Gastos:Cuentas:Gas            $1200        $2700
```

Ahora tiene más sentido, ¿No?

De aquí en adelante, es sólo cosa de mantener el registro, y de ponerse creativo con las consultas que se pueden resolver.

Por ejemplo, con un registro (de mentira :P) para el 2016...
```
$ ledger -f file.ledger stats
Time period: 16-Jan-01 to 16-Dec-31 (365 days)

  Files these postings came from:
    file.ledger

  Unique payees:               8
  Unique accounts:             8

  Number of postings:        172 (0.47 per day)
  Uncleared postings:          0

  Days since last post:       53
  Posts in last 7 days:        0
  Posts in last 30 days:       0
  Posts seen this month:       0
```
puedes tener una idea de como estuvo el año:

```
$ ledger -f file.ledger --begin 2016-01-01 --end 2017-01-01  balance
             $248977  Activos
             $240000    Ahorro Vacaciones
               $8977    Cuenta Corriente
            $1076023  Gastos
             $478650    Cuentas
             $153550      Agua
             $142900      Gas
             $182200      Luz
             $597373    Supermercado
           $-1325000  Ingresos
            $-125000    Pitutos
           $-1200000    Trabajo
--------------------
                   0
```

o saber cuanto gastaste en total en cada una de las cuentas de la casa:
```
$ ledger -f file.ledger --begin 2016-01-01 --end 2017-01-01  register --yearly gastos:cuentas
16-Jan-01 - 16-Dec-31           Gastos:Cuentas:Agua         $153550      $153550
                                Gastos:Cuentas:Gas          $142900      $296450
                                Gastos:Cuentas:Luz          $182200      $478650
```

o incluso cuanto fué el gasto promedio en supermercado:
```
$ ledger -f file.ledger --begin 2016-01-01 --end 2017-01-01  register --average --monthly gastos:supermercado
16-Jan-01 - 16-Jan-31           Gastos:Supermercado          $46567       $46567
16-Feb-01 - 16-Feb-29           Gastos:Supermercado          $50599       $48583
16-Mar-01 - 16-Mar-31           Gastos:Supermercado          $47260       $48142
16-Apr-01 - 16-Apr-30           Gastos:Supermercado          $57038       $50366
16-May-01 - 16-May-31           Gastos:Supermercado          $48703       $50033
16-Jun-01 - 16-Jun-30           Gastos:Supermercado          $78165       $54722
16-Jul-01 - 16-Jul-31           Gastos:Supermercado          $46580       $53559
16-Aug-01 - 16-Aug-31           Gastos:Supermercado          $37390       $51538
16-Sep-01 - 16-Sep-30           Gastos:Supermercado          $49098       $51267
16-Oct-01 - 16-Oct-31           Gastos:Supermercado          $46636       $50804
16-Nov-01 - 16-Nov-30           Gastos:Supermercado          $43579       $50147
16-Dec-01 - 16-Dec-31           Gastos:Supermercado          $45758       $49781
```

Esto es sólo un barniz de todo lo que se puede hacer.


##### Algunas ideas...
Lo anterior es una introducción muy básica de como se puede usar `ledger`.
Pero hay otras cosas que se pueden realizar.
A continuación algunas ideas, que han salido de algunas temas financieros en los que me he topado.


###### Limitar las cuentas que pueden aparecer en el registro
Como a `ledger` le da lo mismo como se llame una cuenta, es muy facil anotar una transaccion en una cuenta equivocada (por ejemplo, que tenga un error de ortografía):
```
$ cat file.ledger
2017-01-01 * Enel
  Gastos:Cuentas:Luz  $10000
  Activos:Cuenta Corriente

2017-02-01 * Enel
  Gastos:Cunetas:Luz  $10000
  Activos:Cuenta Corriente
```

Todo se ve normal, pero al ver el balance aparecen dos cuentas:
```
$ ledger -f file.ledger balance Gastos
              $20000  Gastos
              $10000    Cuentas:Luz
              $10000    Cunetas:Luz
--------------------
              $20000
```

Facil de ver cuando las cuentas son pocas, pero cuando son 100 cuentas distintas, y el registro de balance completo se extiende mucho, es mejor que el error sea más evidente.
`Ledger ` permite restringir las cuentas que se pueden registrar en las transacciones, forzando a definirlas antes de que aparezcan en una transacción:

```
$ cat file.ledger
account Activos:Cuenta Corriente
account Gastos:Cuentas:Luz

2017-01-01 * Enel
  Gastos:Cuentas:Luz  $10000
  Activos:Cuenta Corriente

2017-02-01 * Enel
  Gastos:Cunetas:Luz  $10000
  Activos:Cuenta Corriente
```

así, al ejecutar el reporte, `ledger` indica claramente que hay un error, debido a que aparece una cuenta no declarada.
```
$ ledger --explicit --pedantic -f file.ledger balance Gastos
While parsing file "./file.ledger", line 9:
While parsing posting:
  Gastos:Cunetas:Luz  $10000

Error: Unknown account 'Gastos:Cunetas:Luz'
```

Cuando el registro se extiente harto, esto se agradece.

###### Efectivo, y gastos realizados con él.
Sacar efectivo es simple. Pero registrarlo puede complicarnos un poco. Puede quedar como Activo o como Gasto. Tiene sentido como Activo, si despues se van a registrar **todos** los gastos que se hagan con efectivo. Tiene sentido como Gasto si no nos interesa mucho que es lo que pasa con el efectivo.

Esa es la opción que uso yo. Sigo la opción pragmática, y evito usar efectivo para compras importantes, pero si quiero registrar algún gasto en particular que tuve que realizar con efectivo (¿Gastos con maestros? ¿la ida a la Feria?), se puede registrar el movimiento dentro de los mismos gastos:
```
$ cat file.ledger
2017-02-21 Efectivo
  Gastos:Efectivo  $40000
  Activos:Cuenta Coriente

2016-02-21 Maestro
  Gastos:Maestros  $20000
  Gastos:Efectivo

2017-02-21 Feria
  Gastos:Feria  $8000
  Gastos:Efectivo

```

así, mantenemos el registro de gastos.
```
$ ledger -f file.ledger balance Gastos
              $40000  Gastos
              $12000    Efectivo
               $8000    Feria
              $20000    Maestros
--------------------
              $40000
```

###### Gastos que tengo que hacer... pero aún no he hecho.
Ledger permite marcar las transacciones como **realizadas** (en inglés: *cleared*), con un asterisco (\*) en frente del receptor de la transacción.
Esto permite diferenciar entre transacciones que ya se realizaron, y transacciones que se aún no han finalizado. El ejemplo típico sería el tiempo que pasa entre entregar un cheque y que lo cobren.

Una transacción finalizada:
```
2017-02-21 * Receptor
  Gastos:Foo  $5000
  Activos:Bar
```

y una transacción sin finalizar
```
2017-02-21 Receptor2
  Gastos:Foo  $3000
  Activos:Bar
```

Entonces, 
```
$ cat file.ledger
2017-02-21 * Receptor
  Gastos:Foo  $5000
  Activos:Bar

2017-02-21 Receptor2
  Gastos:Foo  $3000
  Activos:Bar
```

podemos diferenciar si la transacción está finalizada:
```
$ ledger -f file.ledger --cleared register Gastos
17-Feb-21 Receptor              Gastos:Foo                    $5000        $5000
```

o no:
```
$ ledger -f file.ledger --uncleared register Gastos
17-Feb-21 Receptor2             Gastos:Foo                    $3000        $3000
```

Esto es util si quieres proyectar gastos al futuro y ver como se van a mover las finanzas de acuerdo a ese gasto. Cuando el gasto realmente se realice, basta con poner un \* en el registro y listo.

###### Compras en cuotas.
Si usas tarjeta de crédito, a veces se puede suavizar un poco el golpe de compras grandes utilizando la compra en cuotas que normalmente ofrecen los bancos (en especial si son sin intereses [^1] [^2] )

En ese caso, la compra se puede registrar marcando la fecha del pago de cada cuota:
```
$ cat file.ledger
2017-02-20 * Tienda
  Gastos:Compras Irresponsables  $300000
  Deudas:Tarjeta de Credito  -$100000  ; [=2017-03-01]
  Deudas:Tarjeta de Credito  -$100000  ; [=2017-04-01]
  Deudas:Tarjeta de Credito  -$100000  ; [=2017-05-01]
```

Con este registro, puedes saber cuando hiciste la compra:
```
$ ledger -f file.ledger register "Compras Irresponsables"
17-Feb-20 Tienda                ..mpras Irresponsables      $300000      $300000
```

y tambíen puedes ver cuando te toca pagar cada cuota:
```
$ ledger -f file.ledger --effective register "Tarjeta de Credito"
17-Mar-01 Tienda                Deu:Tarjeta de Credito     $-100000     $-100000
17-Apr-01 Tienda                Deu:Tarjeta de Credito     $-100000     $-200000
17-May-01 Tienda                Deu:Tarjeta de Credito     $-100000     $-300000
```

incluso aparece la Cuota si calculas cuanto te va a salir el cargo de la tarjeta un mes en particular.
```
$ ledger -f file.ledger --effective --begin 2017-04-01 --end 2017-05-01 balance Tarjeta
            $-100000  Deudas:Tarjeta de Credito
```

###### Depositos a plazo
Los depósitos a plazo es más facil verlos como 2 transacciones.
La primera, que va desde la cuenta de Activos (eg, la cuenta corriente) a otra cuenta de Activos para ahorro.
```
2017-01-21 * Banco
  Activos:Deposito a Plazo  $100000
  Activos:Cuenta Corriente
```

y la segunda, que va desde la cuenta para ahorros de vuelta a la cuenta corriente. Esta transacción tiene el detalle de que se debe agregar el pequeño ingreso por intereses que entrega el Banco.
```
2017-02-21 * Banco
  Activos:Cuenta Corriente  $100100
  Ingresos:Ganacia de Capitales -$100
  Activos:Deposito a Plazo
```

así, si partimos con algo de dinero:
```
2016-12-31 * Inicio
  Capitales:Dinero  $100000
  Activos:Cuenta Corriente

2017-01-21 * Banco
    Activos:Deposito a Plazo  $100000
    Activos:Cuenta Corriente

2017-02-21 * Banco
    Activos:Cuenta Corriente  $100100
    Ingresos:Ganacia de Capitales  -$100
    Activos:Deposito a Plazo
```

se ven los balances correctamente despues de que el depósito a plazo finalice:
```
$ ledger -f file.ledger balance
             $100100  Activos:Cuenta Corriente
            $-100000  Capital:Dinero
               $-100  Ingresos:Ganacia de Capitales
--------------------
                   0
```

[^1]: Que sean sin intereses no significa que no tengan impuestos asociados. :( 
[^2]: Mejor estrategia es "*pagarse*" las cuotas antes de hacer la compra (esto es: ahorrar), pero esa es otra discusión.