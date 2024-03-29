# Graph Protocol
Graph protocol mainly relies on the [graphql schema file](/subgraph/axolittles/schema.graphql), [subgraph.yaml](/subgraph/axolittles/subgraph.yaml), and the [mapping.ts](/subgraph/axolittles/src/) files. <br><br>
You can test the graph backend using npm. Clone [this repo](https://github.com/graphprotocol/graph-node), cd into `docker` and start the graph server with `docker-compose up`. If you need to start over, delete the `data` directory created inside `docker/`. 
<br><br>
When you deploy a fresh contract, update the `contract address` field in the [subgraph.yaml](subgraph/kelptoken/subgraph.yaml) file.

## install
```
npm install
```

# run things locally

```
npm run codegen
npm run create-local
npm run deploy-local
```

# deploy subgraph
```
npm install -g @graphprotocol/graph-cli
graph init --studio axolittles
graph auth  --studio <subgraph-key>
graph codegen && graph build
graph deploy --studio axolittles
```
