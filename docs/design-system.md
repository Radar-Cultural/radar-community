# Sistema visual

## Idea

Radar Cultural usa la dirección **cartografía cultural viva**. La identidad no presenta un radar
como objeto tecnológico: conecta fragmentos de escena, lectura, taller, cine, música y patrimonio
para mostrar que la cultura ya existe y necesita hacerse visible.

El hero centra la marca y la frase “La cultura sucede. Que nadie se la pierda”. Las fotografías
orbitan el mensaje con profundidad editorial; al desplazarse, caen hacia direcciones distintas,
se desenfocan y se vuelven transparentes. La animación entrega el protagonismo al siguiente relato,
no adorna una pantalla estática.

## Tokens

- Tinta: `#08090d`.
- Blanco de tema claro: `#ffffff`.
- Blanco editorial: `#f7f8fa`.
- Señal: `#3157ff`.
- Vino: `#6b1536`.
- Coral: `#ff5a4f`, reservado para acciones, nodos y pequeños énfasis.

El tema oscuro se comporta como un escenario nocturno; el tema claro como una sala o archivo
diurno. Las fotografías conservan su color y cambian el contexto, contraste y superficies que las
rodean.

## Tipografía y composición

- Títulos: Syne Variable, peso 700–800 y espaciado compacto.
- Texto y controles: Instrument Sans Variable.
- Hero: marca centrada y espacio limpio alrededor del mensaje. Hasta cuatro eventos publicados,
  programados y aún vigentes, con imagen reutilizable, se eligen de una página aleatoria de la
  agenda para ocupar los fragmentos con fecha, crédito y enlace a su ficha. Los espacios sin evento
  conservan una fotografía editorial sin atribuirle una actividad ficticia. La acción principal abre
  la agenda completa.
- Relato de producto: una composición fijada por scroll que convierte un punto en ruta y después en
  red mediante “Encontrar”, “Ubicar” y “Conectar”.
- Datos abiertos: “CULTURA ABIERTA” como texto real de gran escala. Formas inspiradas en libro,
  escenario, onda sonora, cine y artes visuales revelan las letras.
- Cierre: radar parcial recortado por el borde y una sola fotografía circular integrada.
- Botones: rectangulares, jerarquía clara y estado de carga durante desplazamientos iniciados por la
  persona.

Evita bento grids, píldoras decorativas, métricas ficticias, tarjetas repetidas, gradientes
ornamentales, orbes, radares completos y brillos de ciencia ficción.

## Movimiento

- Entrada cinematográfica breve: primero marca, después frase, acciones y fragmentos.
- Caída ambiental muy leve de cada fragmento; el scroll los dispersa, desenfoca y desvanece.
- Narrativa fijada por scroll sólo en escritorio; en móvil conserva el orden natural del documento.
- La ruta se dibuja de forma progresiva y los símbolos culturales revelan la tipografía.
- El radar final usa un movimiento mínimo del sector de barrido.
- Todo el contenido permanece completo con `prefers-reduced-motion`; no hay secciones fijadas ni
  contenido oculto en ese modo.

## Activos

- `frontend/src/assets/fragment-dance.webp`: escena y movimiento.
- `frontend/src/assets/fragment-books.webp`: lectura y archivo.
- `frontend/src/assets/fragment-cinema.webp`: proyección y encuentro.
- `frontend/src/assets/fragment-music.webp`: interpretación musical.
- `frontend/src/assets/hero-day.webp`: arquitectura y patrimonio.
- `frontend/src/assets/community-workshop.webp`: colaboración cultural y taller.

Las fotografías son atmósferas editoriales generadas para la identidad; no son evidencia de
eventos, sedes, fechas o alianzas reales. Los textos, controles, rutas, símbolos y radar se mantienen
como HTML, CSS y SVG.
