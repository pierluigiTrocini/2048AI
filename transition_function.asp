% fase di guess: per ogni answer set deve esserci al massimo una mossa disponibile
% in base agli stati ipotetici in input
% (si esclude a priori la mossa relativa allo stato corrente)
{move(X) : cell(X, _, _, _), X <> "current"} = 1.

dim(N) :- N = #max{X : cell(_, X, _, _)}.
fixed_corner(0, 0).

% CALCOLI PRELIMINARI - per atomi che serviranno nei weak constraints
% determina la cella con valore massimo per la mossa M
max_value(X, Y, Value) :- move(Move), cell(Move, X, Y, Value), Value == #max{V, X, Y : cell(Move, X, Y, V), V <> 0}.

% determina la cella con valore massimo per lo stato corrente
current_max(X, Y, Value) :- cell("current", X, Y, Value), Value == #max{V, X, Y : cell("current", X, Y, V), V <> 0}.

% determinare la distanza manhattan tra max_value e fixed_corner
from_corner(X, Y, Distance) :- max_value(X, Y, _), fixed_corner(Fixed_x, Fixed_y), 
    &abs(X - Fixed_x; Dx), &abs(Y - Fixed_y; Dy), Distance = Dx + Dy.

% determinare la cella con valore massimo più vicina all'angolo
minimum_distance_max_value(X, Y, Distance) :- from_corner(X, Y, Distance), Distance == #min{Dist : from_corner(R, C, Dist)}.

% minimizzare la distanza minima tra max_value e fixed_corner
:~ minimum_distance_max_value(X, Y, Distance). [Distance@1]

% celle adiacenti a max_value (la cella alla minore distanza) devono avere valore maggiore o uguale a Vmax / 2
:~ move(Move), minimum_distance_max_value(Max_x, Max_y, _), cell(Move, Cell_x, Cell_y, Value), max_value(Max_x, Max_y, Vmax),
    Max_x <> Cell_x, Max_y <> Cell_y, &abs(Max_x - Cell_x; Dx), &abs(Max_y - Cell_y; Dy), Dy

% celle non adiacenti a max_value devono avere valore compreso (Value / 2) oppure Value
% minimizzare il numero di celle piene (Value <> 0)