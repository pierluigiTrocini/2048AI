% fase di guess: per ogni answer set deve esserci al massimo una mossa disponibile
% in base agli stati ipotetici in input
% (si esclude a priori la mossa relativa allo stato corrente)
{move(X) : cell(X, _, _, _), X <> "current"} = 1.

dim(N) :- N = #max{X : cell(_, X, _, _)}.
corner(0, 0).
corner(0, N) :- dim(N).
corner(N, 0) :- dim(N).
corner(N, N) :- dim(N).

% si calcola la cella con valore massimo
max_value(Move, X, Y, Value) :- move(Move), cell(Move, X, Y, Value), Value == #max{V : cell(Move, Row, Col, V)}.

% calcolo delle distanze (manhattan) della cella con valore massimo a ogni angolo
from_corner(Max_X, Max_Y, Corner_X, Corner_Y, Distance) :- max_value(_, Max_X, Max_Y, _), corner(Corner_X, Corner_Y),
    &abs(Max_X - Corner_X; DistanceX), &abs(Max_Y - Corner_Y; DistanceY), 
    Distance = DistanceX + DistanceY.

% Minimizzare la distanza (manhattan) tra la cella con valore massimo e l'angolo più vicino
:~ MinimumDistance = #min{Distance : from_corner(_, _, _, _, Distance)}. [MinimumDistance@1]

% Minimizzare la distanza (manhattan) tra coppie di celle con valore (v1 == 2 * v2)
:~ move(M), cell(Move, X, Y, V1), cell(Move, X1, Y1, V2),
    X <> X1, Y <> Y1,
    V1 == 2 * V2,
    &abs(X - X1; Dx), &abs(Y - Y1; Dy), Distance = Dx + Dy. [Distance@1]

% Minimizzare la distanza (manhattan) tra celle dello stesso valore
:~ move(M), cell(Move, X, Y, Value), cell(Move, X1, Y1, Value), 
    X <> X1, Y <> Y1, &abs(X - X1; Dx), &abs(Y - Y1; Dy), 
    D = Dx + Dy. [D@2]


% Massimizzare il punteggio (la somma dei valori delle celle)
:~ Score = #sum{Value : move(M), cell(Move, X, Y, Value)}. [-Score@3]

% Minimizzare il numero di celle non vuote
:~ move(Move), N = #count{X, Y : cell(Move, X, Y, Value)}. [N@3]