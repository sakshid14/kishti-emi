import React from 'react';

interface ProgressBarProps {
  value: number;
  max: number;
  color?: 'blue' | 'green' | 'orange' | 'red';
  showPercentage?: boolean;
  height?: 'sm' | 'md' | 'lg';
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max,
  color = 'blue',
  showPercentage = true,
  height = 'md'
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  
  const colorClasses = {
    blue: 'bg-blue-600',
    green: 'bg-green-600',
    orange: 'bg-orange-600',
    red: 'bg-red-600',
  };

  const heightClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  };

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700">
          ₹{value.toLocaleString()} / ₹{max.toLocaleString()}
        </span>
        {showPercentage && (
          <span className="text-sm text-gray-500">
            {percentage.toFixed(1)}%
          </span>
        )}
      </div>
      <div className={`bg-gray-200 rounded-full overflow-hidden ${heightClasses[height]}`}>
        <div
          className={`${colorClasses[color]} ${heightClasses[height]} rounded-full transition-all duration-300 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;