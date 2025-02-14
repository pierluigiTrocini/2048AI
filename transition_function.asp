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
:~ minimum_distance_max_value(X, Y, Distance). [(Distance*Distance)@1]

% non vorrei che, data una cella con valore V, la cella alla sua destra abbia un valore diverso da V / 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y + 1), V2 <> V / 2. [1@2, X, Y]

% non vorrei che, data una cella con valore V, la cella sotto di essa abbia un valore diverso da V / 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X + 1), V2 <> V / 2. [1@2, X, Y]

% non vorrei che, data una cella con valore V, la cella alla sua sinistra abbia un valore diverso da V * 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y - 1), V2 <> V * 2. [1@2, X, Y]

% non vorrei che, data una cella con valore V, la cella sopra ad essa abbia un valore diverso da V * 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X - 1), V2 <> V * 2. [1@2, X, Y]

% data la mossa Move, non vorrei che minimum_distance_max_value abbia celle sopra di essa
:~ move(Move), minimum_distance_max_value(X, Y, _), cell(Move, X, Y1, _), Y1 == (Y - 1). [1@3, X, Y]

% data la mossa Move, non vorrei che minimum_distance_max_value abbia celle a sinistra di essa
:~ move(Move), minimum_distance_max_value(X, Y, _), cell(Move, X1, Y, _), X1 == (X - 1). [1@3, X, Y]



% minimizzare il numero di celle piene (Value <> 0)
:~ move(Move), N = #count{X, Y : cell(Move, X, Y, Value), Value <> 0}. [N@4]