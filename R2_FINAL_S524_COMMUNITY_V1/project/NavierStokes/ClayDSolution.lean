import ClayStatement.Bridge
import NavierStokes.ComparatorCompleteSolution
import NavierStokes.ComparatorSolution

namespace NavierStokes.ClayD
theorem clay_D : Clay.NavierStokes.StatementD :=
  Clay.NavierStokes.Bridge.optionD_imp_statementD NavierStokes.Comparator.navier_stokes_breakdown_periodic
end NavierStokes.ClayD
