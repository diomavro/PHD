import React, { useState } from 'react';
import { Trash2, Plus, DollarSign } from 'lucide-react';

interface Employee {
  id: string;
  name: string;
  // `hours` kept for compatibility but weekly hours are stored in `hoursGrid`
  hours: number;
}

interface CalculationResult {
  employee_name: string;
  hours: number;
  share_percentage: number;
  tip_amount: number;
}

interface SaveResponse {
  id: number;
  message: string;
}

const TipDistribution: React.FC = () => {
  const [totalTips, setTotalTips] = useState<string>('');
  const [employees, setEmployees] = useState<Employee[]>([
    { id: '1', name: '', hours: 0 }
  ]);
  // hoursGrid[employeeId][dateString] = hours for that day
  const [hoursGrid, setHoursGrid] = useState<Record<string, Record<string, number>>>({});
  // selectedDate will be used to compute the week (start from Monday)
  const [weekStart, setWeekStart] = useState<string>(() => {
    const d = new Date();
    // find Monday of current week
    const day = d.getDay();
    const diff = (day === 0 ? -6 : 1) - day; // make Monday the start
    const monday = new Date(d);
    monday.setDate(d.getDate() + diff);
    return monday.toISOString().slice(0, 10);
  });
  const [results, setResults] = useState<CalculationResult[]>([]);
  const [isSaved, setIsSaved] = useState(false);
  const [error, setError] = useState<string>('');

  const addEmployee = () => {
    const newId = (Math.max(...employees.map(e => parseInt(e.id)), 0) + 1).toString();
    setEmployees([...employees, { id: newId, name: '', hours: 0 }]);
    setHoursGrid(prev => ({ ...prev, [newId]: {} }));
  };

  const removeEmployee = (id: string) => {
    if (employees.length > 1) {
      setEmployees(employees.filter(e => e.id !== id));
      setHoursGrid(prev => {
        const copy = { ...prev };
        delete copy[id];
        return copy;
      });
    }
  };

  const updateEmployee = (id: string, field: 'name' | 'hours', value: string | number) => {
    setEmployees(employees.map(e => 
      e.id === id ? { ...e, [field]: value } : e
    ));
  };

  // Ensure hoursGrid has entries when employees or weekStart changes
  React.useEffect(() => {
    setHoursGrid(prev => {
      const next = { ...prev } as Record<string, Record<string, number>>;
      const dates = getWeekDates(weekStart);
      employees.forEach(emp => {
        if (!next[emp.id]) next[emp.id] = {};
        dates.forEach(d => {
          if (typeof next[emp.id][d] !== 'number') next[emp.id][d] = 0;
        });
      });
      // remove keys for removed employees
      Object.keys(next).forEach(k => {
        if (!employees.find(e => e.id === k)) delete next[k];
      });
      return next;
    });
  }, [employees, weekStart]);

  const updateHours = (employeeId: string, dateStr: string, value: number) => {
    setHoursGrid(prev => ({
      ...prev,
      [employeeId]: {
        ...(prev[employeeId] || {}),
        [dateStr]: value,
      }
    }));
  };

  function getWeekDates(startIso: string) {
    const start = new Date(startIso + 'T00:00:00');
    const dates: string[] = [];
    for (let i = 0; i < 7; i++) {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      dates.push(d.toISOString().slice(0, 10));
    }
    return dates;
  }

  const calculateTips = async () => {
    setError('');
    setIsSaved(false);
    
    // Validation
    if (!totalTips || parseFloat(totalTips) <= 0) {
      setError('Please enter a valid total tips amount');
      return;
    }

    // derive total hours per employee from hoursGrid
    const employeesWithTotals = employees.map(e => {
      const perDay = hoursGrid[e.id] || {};
      const total = Object.values(perDay).reduce((s, v) => s + (v || 0), 0);
      return { id: e.id, name: e.name, totalHours: total };
    });

    const validEmployees = employeesWithTotals.filter(e => e.name && e.totalHours > 0);
    if (validEmployees.length === 0) {
      setError('Please add at least one employee with hours worked');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            total_tips: parseFloat(totalTips),
            employees: validEmployees.map(e => ({
              name: e.name,
              hours: e.totalHours
            }))
          }),
      });

      if (!response.ok) {
        throw new Error('Failed to calculate tips');
      }

      const data: CalculationResult[] = await response.json();
      setResults(data);

      // Save to database
      const saveResponse = await fetch('http://localhost:8000/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            total_tips: parseFloat(totalTips),
            employees: validEmployees.map(e => ({
              name: e.name,
              hours: e.totalHours
            })),
            results: data
          }),
      });

      if (saveResponse.ok) {
        setIsSaved(true);
      }
    } catch (err) {
      setError('Error calculating or saving tips: ' + (err as Error).message);
    }
  };

  // total hours across the whole grid
  const totalHours = Object.values(hoursGrid).reduce((sumEmp, perDay) => {
    return sumEmp + Object.values(perDay).reduce((s, v) => s + (v || 0), 0);
  }, 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <DollarSign className="text-green-600" />
            Tip Distribution Calculator
          </h1>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {isSaved && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              Successfully saved to database!
            </div>
          )}

          {/* Total Tips Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Total Tips for the Week ($)
            </label>
            <input
              type="number"
              step="0.01"
              value={totalTips}
              onChange={(e) => setTotalTips(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter total tips"
            />
          </div>

          <div className="mb-4 text-sm text-gray-700">
            Total hours for selected week: <span className="font-medium">{totalHours.toFixed(2)} hrs</span>
          </div>

          {/* Weekly Hours Grid */}
          <div className="mb-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-3">
              <div className="flex items-center gap-3">
                <h2 className="text-xl font-semibold text-gray-800">Weekly Hours</h2>
                <label className="text-sm text-gray-600">Week start (Monday):</label>
                <input
                  type="date"
                  value={weekStart}
                  onChange={(e) => setWeekStart(e.target.value)}
                  className="px-2 py-1 border border-gray-300 rounded"
                />
              </div>
              <div>
                <button
                  onClick={addEmployee}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  <Plus size={20} />
                  Add Employee
                </button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="px-3 py-2 text-left text-sm font-semibold text-gray-700">Date</th>
                    {employees.map(emp => (
                      <th key={emp.id} className="px-3 py-2 text-center align-top border-l">
                        <div className="flex flex-col items-center gap-2">
                          <input
                            type="text"
                            value={emp.name}
                            onChange={(e) => updateEmployee(emp.id, 'name', e.target.value)}
                            placeholder="Name"
                            className="w-28 text-sm px-2 py-1 border border-gray-300 rounded"
                          />
                          <button
                            onClick={() => removeEmployee(emp.id)}
                            disabled={employees.length === 1}
                            className={`p-1 rounded hover:bg-red-100 transition ${employees.length === 1 ? 'opacity-50 cursor-not-allowed' : ''}`}
                            title="Remove employee"
                          >
                            <Trash2 size={14} className="text-red-600" />
                          </button>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {getWeekDates(weekStart).map(dateStr => {
                    const display = new Date(dateStr + 'T00:00:00').toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' });
                    return (
                      <tr key={dateStr} className="border-b hover:bg-gray-50">
                        <td className="px-3 py-2 text-sm text-gray-700 font-medium">{display}</td>
                        {employees.map(emp => (
                          <td key={emp.id} className="px-3 py-2 text-center border-l">
                            <input
                              type="number"
                              step="0.25"
                              min={0}
                              value={(hoursGrid[emp.id] && hoursGrid[emp.id][dateStr]) ?? 0}
                              onChange={(e) => updateHours(emp.id, dateStr, parseFloat(e.target.value) || 0)}
                              className="w-20 mx-auto px-2 py-1 border border-gray-300 rounded text-center"
                            />
                          </td>
                        ))}
                      </tr>
                    );
                  })}
                </tbody>
                <tfoot>
                  <tr className="bg-gray-100 font-semibold">
                    <td className="px-3 py-2">Total</td>
                    {employees.map(emp => {
                      const empTotal = (getWeekDates(weekStart).reduce((s, d) => s + ((hoursGrid[emp.id] && hoursGrid[emp.id][d]) || 0), 0));
                      return (
                        <td key={emp.id} className="px-3 py-2 text-center border-l">{empTotal.toFixed(2)} hrs</td>
                      );
                    })}
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>

          {/* Calculate Button */}
          <button
            onClick={calculateTips}
            className="w-full py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition text-lg"
          >
            Calculate & Save
          </button>

          {/* Results */}
          {results.length > 0 && (
            <div className="mt-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Results</h2>
              <div className="bg-blue-50 rounded-lg p-6">
                <div className="grid gap-4">
                  {results.map((result, index) => (
                    <div key={index} className="bg-white rounded-lg p-4 shadow">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="font-semibold text-lg text-gray-800">
                            {result.employee_name}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {result.hours} hours ({result.share_percentage.toFixed(2)}%)
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-bold text-green-600">
                            ${result.tip_amount.toFixed(2)}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TipDistribution;
