Al descargar el documento hay que entrar desde la terminal a la carpeta 2 y ahi activar el entorno virtual con el siguiente comando venv\Scripts\activate
En el caso de querer cerrar el entorno solo hay que poner deactivate
Una vez que inicies el entorno pones el siguiente comando python manage.py runserver
una vez que empice a correr el puerto, entraras a la ruta http://127.0.0.1:8000/shorten/
Esta ruta te abrirá la vista principal en html, css y js donde podras iniciar sesión, ingresar los Urls y que te devuelvan el Url cortado
Para iniciar sesión puedes ingresar con el correo ejemplo@gmail.com y la contraseña 123456, o con el usuario Diego y la contraseña 369807
Al iniciar sesión podras ver todos los urls creados con anterioridad tanto privados como publicos públicos.
En el caso de querer verlo todo desde el swagger sera desde la siguiente ruta http://127.0.0.1:8000/swagger/
Donde pondras iniciar sesión, registrarte, ver todos los registros, borrar, editar, crear y buscar uno en especial.
En el caso de querer ver el panel de control sera desde la ruta http://127.0.0.1:8000/admin/login/?next=/admin/
Para ingresar sera con el usuario Diego y la contraseña 369807.
