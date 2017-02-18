+++
title = "on ledger"
draft = true
date = "2017-02-11T14:49:24-03:00"

+++

Llega un punto en el que hay ponerse serio con la plata. 

No es necesariamente porque te falte, pero porque sientes que podrías gastar mejor la que tienes, o estás pensando en un proyecto que requiere de un poco más de orden con los gastos del que tienes ahora.
Llevar un presupuesto no te vendría mal, es solo cuestión de... llevarlo.

¿Cierto?

La respuesta obvia para quienes están acostumbrados a trabajar con un computador es una planilla de cálculo. [Microsoft Excel](https://products.office.com/es-cl/excel), [Google Spreadsheet](https://www.google.com/intl/es/sheets/about/), [Apple Numbers](http://www.apple.com/cl/numbers/), o incluso [LibreOffice Calc](https://es.libreoffice.org/descubre/calc/). El problema que tienen es que las planillas de calculo son demasiado genéricas para llevar finanzas, y hay que amoldarlas a lo que uno quiere. Cuando no tienes claro que es lo que quieres, esto me terminó complicando la vida más de lo que valía la pena.

Además, después de un tiempo de registrar y registrar los ingresos y los gastos, la planilla se vuelve un poco dificil de manejar. Al menos eso fué lo que me pasó a mi.

Otra opción es [GNUCash](https://es.wikipedia.org/wiki/GnuCash). GnuCash, por si no lo conocen, es un software para manejo de finanzas. Está pensado para finanzas personales, y también para manejar empresas pequeñas. Pero la verdad nunca me acostumbré. Puede ser porque era la primera vez que me encontré con el [registro de partida doble](https://es.wikipedia.org/wiki/Partida_doble).

Otro problema que tenía con la planilla, y en menor medida con el archivo de GNUCash, era que el archivo vivía en una sóla parte. Claro, ahora con Dropbox, Google Drive, Onedrive o similares, es más simple, pero no siempre fué facil mantener una copia definitiva de los archivos que fuese sencillo editar en todas partes. Menos si usas Windows en el trabajo, y Linux en la casa.

Por el trabajo, estaba acostumbrado a vivir en la Linea de Comando de Sistemas Linux, y por casualidad me topé con [Ledger](http://www.ledger-cli.org/), y como estaba aún experimentando con "soluciones" a mi problema, me dí el trabajo de pasar un poco de la información al formato de Ledger y probarlo.

##### `Ledger`... en serio?

Primero lo primero: Ledger no es para cualquiera, es una solución complicada para un problema complicado.

En simple, es una herramienta para hacer calculos en un registro de partida doble.



```
$ ledger balance
```