## Sistema de Recuperació de Información

**Nelson Robin Mendoza Alvarez** *C-411*

### Resumen

Los Sistemas de Recuperación de Información (SRI) constituyen una rama importante en las ciencias de la computación. En el presente trabajo se realizará un análisis a diferentes modelos a través de su creación, transitando por todas las fases de la recuperación de información: procesamiento de la consulta, representación de los documentos, funcionamiento del motor de búsqueda y la obtención de los resultados. Al final se evaluarán los modelos con las diferentes métricas estudiadas en clases: precisión, recobrado y medida F1.

### Abstract

Information Retrieval Systems (IRS) constitute an important branch of computer science. In the present work, an analysis will be carried out on different models through their creation, going through all the phases of information retrieval: processing of the query, representation of the documents, operation of the search engine and obtaining the results. At the end, the models will be evaluated with the different metrics studied in class: precision, recovery and F1 measurement.

### Introducción

Desde la antigüedad, desde la Alejandría de Tolomeo, hasta las bibliotecas monásticas de la Edad Media, se definió con claros enunciados, la necesidad del  desarrollar métodos y técnicas, que no solo permitieran el control y  conservación de las colecciones, sino también la identificación de cada  de uno de sus ejemplares con el objetivo de recuperarlos correctamente. A pesar de que, desde entonces, se utilizaron técnicas para el manejo de  los títulos y responder a las escasas necesidades de información de la  época, no fue, sino con el desarrollo científico y la especialización, que se maximizó la exigencia sobre estos métodos en aras de  satisfacer necesidades cada vez más puntuales, en medio de un  conocimiento científico en constante expansión.

La invención en 1946 de las tecnologías computacionales fue de  progresiva e inmediata aplicación en la naciente esfera de la  información, especialmente para solucionar las preocupaciones dominantes en ese lapso de explosión documental, sobre como localizar y buscar  información puntualmente.

La recuperación de información es el proceso de obtener recursos del sistema de información que son relevantes para una necesidad de información a partir de una colección de esos recursos.

Cada modelo de recuperación de información presenta un conjunto de etapas. Una de estas es el procesamiento de la consulta, en el que se toma la consulta y se representa de forma adecuada para que el modelo definido la procese. La representación de los documentos, es la fase en la que se procesan los documentos para obtener una representación que esté acorde con el modelo que se utilizará. El funcionamiento del motor de búsqueda, incluye llevar a la práctica el modelo a utilizar. Y por último, la obtención de resultados, es el punto en el que aquellos documentos recuperados son dispuestos ante el usuario a manera de ranking a partir de una puntuación determinada por el nivel de significación de cada documento dada la consulta realizada.

### Dependencias

- python 3.x
- numpy
- pickle
- nltk
- PyQt5

### ¿Cómo ejecutar el proyecto?

1. Situarse dentro de la carpeta "Project SRI"
2. Abrir una terminal en esa ubicación
3. Correr el comando: python3 appSRI.py

### Modelos

#### Modelo Vectorial

El primer aspecto a tener en cuenta es la forma de representar la colección de archivos y la consulta. En el caso de los primeros, se calcula el peso de cada término en los documentos mediante la frecuencia de los mismos ($tf$) a través de la ecuación:

$tf_{ij}=\dfrac{n_{ij}}{máx_k{n_{kj}}}$

donde $n_{ij}$ representa las veces que ocurre el término $i$ en el documento $j$ y, $tf_{ij}$ el valor del $tf$ del término $i$ en el documento $j$ y; el ı́ndice de frecuencia invertida ($idf$), dado por:

$idf_i=log\left(\dfrac{N}{n_i}\right)$

donde $N$ es la cantidad de documentos de la colección y $n_i$ es la cantidad de documentos que contienen al término $i$; de esta forma cada documento se representa como un vector de pesos con una cantidad de componentes igual a la cantidad de terminos del alfabeto. En el caso de la consulta $tf$ indica la frecuencia de cada término en la misma, mientras que $idf$ mantiene el mismo significado que en el caso de los documentos. 

Formalmente para cada documento $i$ se define el peso del término $j$ como $w_{ij}$ dónde:

$w_{ij}=tf_{ij}\cdot idf_j$

mientras que en la consulta $q$:

$w_{qj}=(\alpha + (1-\alpha)\cdot tf_{qj})\cdot idf_j$

donde $\alpha$ representa un valor de suavisado para minimizar la contribución de la frecuencia del término al peso del mismo en la consulta.

Luego la similitud de los documentos según la consulta está dada por:

$sim(d_i,q)=\dfrac{\sum_{j=1}^nw_{ij}\cdot w_{qj}}{\sqrt{\sum_{j=1}^nw_{ij}^2}\cdot\sqrt{\sum_{j=1}^nw_{qj}^2}}$.

#### Modelo Booleano

En el Modelo Booleano los términos indexados toman valores binarios, es decir, que solo se tiene en cuenta si el término aparece o no en el documento. La consulta se define como una expresión del álgebra booleana con los operadores NOT, AND y OR. Para procesar la consulta, esta se expresa de manera equivalente como una disyunción de conjunciones lo que nos permite establecer una correspondencia directa entre la consulta y los vectores de términos indexados que representan a los documentos.

Por tanto la similitud entre una consulta y un documento está dado por:
$$
sim(d_j,q)=\left\{
	\begin{array}{c}
		1\quad si\quad \exists\overrightarrow{q_{cc}}:(\overrightarrow{q_{cc}}\in\overrightarrow{q_{fnd}})\wedge (\forall_{k_i},g_i(\overrightarrow{d_j})=g_i(\overrightarrow{q_{cc}}))\\
		0\quad en\quad otro\quad caso.
	\end{array}
\right.
$$


#### Modelo Fuzzy

En el Modelo Fuzzy, al igual que el Booleano, los términos indexados toman valores binarios, es decir, que solo se tiene en cuenta si el término aparece o no en el documento. La consulta se define como una expresión del álgebra booleana con los operadores NOT, AND y OR. Para procesar la consulta, esta se expresa de manera equivalente como una disyunción de conjunciones lo que nos permite establecer una correspondencia directa entre la consulta y los vectores de términos indexados que representan a los documentos.

Para el calculo del ranking de este modelo es necesario calcular la correlación de cada par de términos $k_i$ y $k_j$ de la siguiente forma:

$c_{ij}=\dfrac{n_{ij}}{n_i+n_j-n_{ij}}$

donde $n_i(n_j)$ es la cantidad de documentos en los que aparece el término $k_i(k_j)$ y $n_{ij}$ es la cantidad de documentos que contienen a ambos términos.

Este modelo define un conjunto difuso para cada término indexado y cada documento tendrá un grado de pertenencia a cada uno de estos conjuntos dado por:

$\mu_{ij}=1-\prod_{k_l\in d_j}(1-c_{il})\\$

Luego la similitud entre una consulta y un documento está dado por:

$sim(d_j,q)=1-\prod_{i=1}^p(1-\mu_{cc_{ij}})\\$

donde $p$ es la cantidad de componentes conjuntivas de $q$ y $\mu_{cc_{ij}}$ representa el grado de pertenencia de $d_j$ a la componente conjuntiva i-ésima de $q$ y se calcula de la siguiente manera:

$\mu_{cc_{ij}}=\prod_{l=1}^nt_l\\$

donde
$$
t_l=\left\{
	\begin{array}{c}
		\mu_{ij},\,si\;el\;término\;l\;aparece\;en\;cc_l\\
		1-\mu_{ij},\,si\;el\;término\;l\;no\;aparece\;en\;cc_l\\
	\end{array}
\right.
$$

### Mediciones

Las medidas que se utilizaron para evaluar los modelos fueron:

**Precisión:**

Esta busca que la mayor parte de los documentos recuperados sean relevantes y se calcula de la siguiente forma:

$P=\dfrac{|RR|}{|RR\cup RI|}$

donde $RR$ son los documentos recuperados que son relevantes y $RI$ es el conjunto de documentos recuperados que son irrelevantes.

**Recobrado:**

Esta busca recuperar la mayor cantidad documentos relevantes y se calcula de la siguiente forma:

$R=\dfrac{|RR|}{|RR\cup NR|}$

donde $NR$ es el conjunto de documentos relevantes que no fueron recuperados.

**Medida F1:**

Es una medida que armoniza Precisión y Recobrado y se calcula de la siguiente forma:

$F1=\dfrac{2PR}{P+R}=\dfrac{2}{\dfrac{1}{P}+\dfrac{1}{R}}$.

### Estructura del proyecto:

En el proyecto se presentan varios módulos o bloques de código fundamentales:

**text_processor** contiene la clase *Cleaner* que se encarga de limpiar el texto, es decir, eliminar los caracteres especiales, los signos de puntuación, llevar las palabras a su raíz, etc. Quedándonos solamente con los tokens que contienen la información del texto. Para la realización de esta tarea nos apoyamos en la biblioteca de python NLTK, designada al procesamiento del lenguaje natural que nos facilita el proceso de tokenizar el documento.

En **corpus** se encuentra la clase *Corpus* que se encarga de tomar los documentos, mandarlos a tokenizar y se crean las tablas que utilizarán los diferentes modelos. Este contiene:

- Un diccionario cuya llave es el *id* de un documento y su valor es la dirección en memoria de este.(docs_id)
- Un diccionario cuya llave es un término y su valor es una lista de los documentos en los que aparece.(index)
- Un diccionario donde las llaves son pares de elementos, donde el primero es un término y el segundo es el identificador de un documento y su valor la frecuencia normalizada del término ($tf$) en el documento.(doc_tf)
- Un diccionario donde la llave es un término y el valor la ocurrencia del término en todos los documentos ($idf$).(idf)
- Un diccionario donde la llave es un término y el valor su peso según el modelo vectorial.(doc_weights)
- Un diccionario donde la llave es el $id$ de un documento y el valor su norma según los pesos de sus términos.(doc_norm)
- Un diccionario donde las llaves son pares de elementos, donde el primero es un término y el segundo es el identificador de un documento y su valor es el peso de ese término en el documento según el modelo fuzzy.(fuzzy)

El **vectorial_model** presenta la clase *VectorialModel* que tiene la tarea de mandar a tokenizar la consulta, calcular la frecuencia y los pesos de sus términos, así como su norma y recuperar los $n$ documentos más relevantes ($n$ está dado por la variable $limit$ que tiene como valor predeterminado 15).

El **boolean_model** presenta la clase *BooleanModel* que tiene la tarea de mandar a tokenizar la consulta y recuperar $n$ documentos que contengan estos mismos tokens ($n$ está dado por la variable $limit$ que tiene como valor predeterminado 15).

El **fuzzy** presenta la clase *FuzzyModel* que tiene la tarea de mandar a tokenizar la consulta y recuperar los $n$ documentos más relevantes ($n$ está dado por la variable $limit$ que tiene como valor predeterminado 15).

Los conjuntos de documentos que serán utilizados son *corpus_cran* y *corpus_med* situados en la carpeta *corpus*.

Para realizar las evaluaciones de los modelos, en la carpeta *queries_rel* se encuentran los archivos: *cran.qry* y *MED.QRY* poseen diversas consultas a los corpus CRAN y MED respectivamente, y en los archivos *cranqrel* y *MED.REL* podemos ver los documentos relevantes a dichas consultas. Y los modelos son evaluados a través de *medicion.py*.

### Interfaz

<img src="/home/spnelson/Imágenes/Captura de pantalla de 2022-12-18 20-55-37.png" style="zoom: 50%;" />

Aquí se eligirá el modelo y el cuerpo de documentos que se desea utilizar

<img src="/home/spnelson/Imágenes/Captura de pantalla de 2022-12-18 20-57-55.png" style="zoom:50%;" />

Aquí se insertará la consulta y obtendremos las direcciones en memoria de los documentos recuperados.



### Concluciones

Luego de evaluar los modelos analizados podemos observar que el modelo que presentó los mejores resultados de las diferentes mediciones en cada uno de los conjuntos de documentos fue el Modelo Vectorial, luego el Fuzzy, siendo el modelo Booleano el que presentó el peor resultado. 

En las siguientes gráficas se muestran los resultados de las mediciones realizadas a los modelos en diferentes consultas:

![](/home/spnelson/Documentos/SRI/Evaluación Cran.png)

![Evaluación Med](/home/spnelson/Documentos/SRI/Evaluación Med.png)

También se debe aclarar que debido a que el modelo Fuzzy debe realizar una correlación entre todos los pares términos indexados, es muy poco eficiente en cuanto al tiempo en cargar los conjuntos de documentos.