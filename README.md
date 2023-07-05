![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg) [![BuyMeCoffee][buymecoffeebedge]][buymecoffee]

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667


# Tabela FIPE Brasil Sensor Component

![image](https://github.com/hudsonbrendon/ha_fipe_brasil/assets/5201888/da446b0f-82e3-4c3c-9152-071b942c2b8a)


Um componente customizado para ter acesso aos dados da tabela FIPE diretamente no Home assistant

## Instalação

### Instação via HACS

Tenha o HACS instalado, isso permitirá que você atualize facilmente.

Adicionar Ingresso ao HACS pode ser usando este botão:

[![image](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hudsonbrendon&repository=ha_fipe_brasil&category=integration)

Caso o botão acima não funcione, adicione `https://github.com/hudsonbrendon/ha_fipe_brasil` como um repositório customizado do tipo Integration no HACS.

- Clique em Instalar na integração `Tabela FIPE Brasil`.
- Reinicie o Home Assistant.

### Manual installation

- Copie a pasta `fipe` de [latest release](https://github.com/hudsonbrendon/ha_fipe_brasil/releases/latest) para o diretório `<config dir>/custom_components/`.
- Reinicie o Home Assistant.

## Configuração

Adicionar o Ingresso à sua instância do Home Assistant pode ser feito por meio da interface do usuário usando este botão:

[![image](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=fipe)

### Configuração Manual

Se o botão acima não funcionar, você também pode executar as seguintes etapas manualmente:

- Navegue até sua instância do Home Assistant.
- Na barra lateral, clique em Configurações.
- No menu Configuração, selecione: Dispositivos e serviços.
- No canto inferior direito, clique no botão Adicionar integração.
- Na lista, pesquise e selecione `Tabela FIPE Brasil`.
- Siga as instruções na tela para concluir a configuração.

# Exibindo os dados

Para exibição dos dados, recomendo a utilização do card [flex-table-card](https://github.com/custom-cards/flex-table-card), instale via hacs e adicione a configuração abaixo (Lembrando de substituir sensor.cinepolis pelo seu sensor configurado) em um manual card:

```yaml
type: custom:flex-table-card
title: Tabela FIPE
entities:
  include: sensor.modelo
columns:
  - name: Modelo
    attr_as_list: data
    modify: x.modelo
  - name: Preço
    attr_as_list: data
    modify: x.valor
  - name: Ano
    attr_as_list: data
    modify: x.anoModelo
```

O código acima irá gerar algo como isso:

![image](https://github.com/hudsonbrendon/ha_fipe_brasil/assets/5201888/d303c7ce-27fc-4a45-a876-743fbf670232)

# Debugand

```yaml
logger:
  default: info
  logs:
    custom_components.ha_fipe_brasil: debug
```

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667
