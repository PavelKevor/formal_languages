### graph_database language documentation

- connect [name] - You can connect to database.

Example:
```sh
connect '/home/fl/graphs'
```
- select [objective] [graph] - You can take objective from graph.


--Objective types:
   1) count - return number of graphs edges.
   2) edges - return all edges (v, e, u)  from graph.

Example:
```sh
select count 'graph1'
select edges 'graph2'
```
[graph] can be a 1)name, 2)graph intersection or 3)graph intersection.

1) If you type graph name, graph with this name will load from your database.

2) You can intersect graphes - [graph] intersect [graph].

Example:
```sh
select edges graph1 intersect 'graph2'
```
3) If you type regular expression,you will take regexp with given pattern. It should be in  {}.

In regular expression you can use:
- alt - alternative plus.
- star - operator *.
- plus - one or more.
- option - optional character.
- conc - concatination.

Example:
```sh
select count from 'graph' intersect {'a' plus conc 'b'}
select count from 'graph' intersect {'a' option conc 'b' conc 'c' plus}
select edges from 'graph' intersect {('a' alt 'b') star conc 'c' plus conc 'd' plus}
```


