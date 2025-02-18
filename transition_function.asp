% fase di guess: per ogni answer set deve esserci al massimo una mossa disponibile
% in base agli stati ipotetici in input
% (si esclude a priori la mossa relativa allo stato corrente)
{move(X) : cell(X, _, _, _), X <> "current"} = 1.

fixed_corner(1, 1).

% CALCOLI PRELIMINARI - per atomi che serviranno nei weak constraints
% determina la cella con valore massimo per la mossa M
max_value(Max_X, Max_Y, Value) :- move(Move), cell(Move, Max_X, Max_Y, Value), Value == #max{V, X, Y : cell(Move, X, Y, V), V <> 0}.

% determinare la distanza manhattan tra max_value e fixed_corner
from_corner(X, Y, Distance) :- max_value(X, Y, _), fixed_corner(Fixed_x, Fixed_y), 
    &abs(X - Fixed_x; Dx), &abs(Y - Fixed_y; Dy), Distance = Dx + Dy.

% determinare la cella con valore massimo più vicina all'angolo
minimum_distance_max_value(X, Y, Distance) :- from_corner(X, Y, Distance), Distance == #min{Dist : from_corner(R, C, Dist)}.

% determinare, data la mossa Move, il numero di celle con valore diverso da zero
non_zero_cells(N) :- move(Move), N = #count{X, Y : cell(Move, X, Y, V), V <> 0}.

% WEAK CONSTRAINTS
% minimizzare la distanza minima tra max_value e fixed_corner
:~ minimum_distance_max_value(_, _, Distance), Distance <> 0. [(Distance*Distance)@1]

% non vorrei che, data una cella con valore V, la cella alla sua destra abbia un valore diverso da V / 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y + 1), V2 <> V / 2. [1@2, X, Y]
% non vorrei che, data una cella con valore V, la cella alla sua destra abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y + 1), V2 <> V. [1@2, X, Y]

% non vorrei che, data una cella con valore V, la cella sotto di essa abbia un valore diverso da V / 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X + 1), V2 <> V / 2. [1@2, X, Y]
% non vorrei che, data una cella con valore V, la cella sotto di essa abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X + 1), V2 <> V. [1@2, X, Y]

% non vorrei che, data una cella con valore V, la cella alla sua sinistra abbia un valore diverso da V * 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y - 1), V2 <> V * 2. [1@2, X, Y]
% non vorrei che, data una cella con valore V, la cella alla sua sinistra abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y - 1), V2 <> V. [1@2, X, Y]

% non vorrei che, data una cella con valore V, la cella sopra ad essa abbia un valore diverso da V * 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X - 1), V2 <> V * 2. [1@2, X, Y]
% non vorrei che, data una cella con valore V, la cella sopra ad essa abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X - 1), V2 <> V. [1@2, X, Y]

% merging: non vorrei che, date due celle adiacenti, dello stato "current", con valori uguali, non esista una cella
% con valore doppio sulla stessa riga (o sulla stessa colonna) nella griglia della mossa Move
merged_cell_x(X, Y, Y2, Move) :- cell("current", X, Y, V), cell("current", X, Y2, V),
    &abs(Y - Y2; Dy), Dy == 1,
    move(Move), cell(Move, X, _, V2), V2 == V * 2.

merged_cell_y(Y, X, X2, Move) :- cell("current", X, Y, V), cell("current", X2, Y, V),
    &abs(X - X2; Dx), Dx == 1,
    move(Move), cell(Move, _, Y, V2), V2 == V * 2.

:~ cell("current", X, Y, V), cell("current", X, Y2, V), V <> 0, not merged_cell_x(X, Y, Y2). [1@3, Y, Y2]
:~ cell("current", X, Y, V), cell("current", X2, Y, V), V <> 0, not merged_cell_y(X, Y, X2). [1@3, X, X2]


% minimizzare il numero di celle piene (valore diverso da 0)
:~ non_zero_cells(N). [N@4]

#show move/1.
#show non_zero_cells/1.
#show merged_cell_x/4.
#show merged_cell_y/4.