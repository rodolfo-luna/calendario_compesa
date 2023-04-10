<h1 align="center"> Calendario de abastecimento Compesa </h1>

Script para extração dos dados do calendário de abastecimento da Compesa.

O Script extrai os dados do calendário da Compesa da região escolhida e manda uma mensagem de texto no Telegram para usuários listados.

O URL foi extraída através das requisições feitas pelo calendário de abastecimento: https://servicos.compesa.com.br/calendario-de-abastecimento-da-compesa/.

Duas URLs são utilizadas, uma para extrair o calendário de abastecimento e outra para o calendário de manutenção.

Exemplos de URLs:

Calendário de abastecimento da Avenida Caxangá para o mês de Abril/2023: https://geo.compesa.com.br:6443/arcgis/rest/services/Calendario/Calendario/MapServer/5/query?f=json&where=(ID%3D%27REDIS8B%27)%20AND%20(DATEPART(MONTH%2CInicio)%3D%2704%27%20OR%20DATEPART(MONTH%2CTermino%20)%3D%2704%27)%20AND%20(DATEPART(YEAR%2CInicio)%3D%272023%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=Inicio%2CTermino%2Ccolapso

Calendário de mantenção da Avenida Caxangá para o mesmo mês: https://geo.compesa.com.br:6443/arcgis/rest/services/Calendario/Calendario/MapServer/2/query?f=json&where=(ID_AREA_ABASTECIMENTO%3D%27REDIS8B%27)%20AND%20(DATEPART(MONTH%2CINICIO_PREVISTO)%3D%2704%27%20OR%20DATEPART(MONTH%2CTERMINO_PREVISTO%20)%3D%2704%27)%20AND%20(DATEPART(YEAR%2CINICIO_PREVISTO)%3D%272023%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=INICIO_PREVISTO%2CTERMINO_PREVISTO%2CDESCRICAO_SERVICO

![Captura de tela em 2023-04-10 17-01-19](https://user-images.githubusercontent.com/83115714/230987228-b7bddc4b-4fe3-4111-9b0b-5819839c7c04.png)

![manut](https://user-images.githubusercontent.com/83115714/230987388-f578fe8c-f581-4ad2-a451-05e9716a328b.png)
