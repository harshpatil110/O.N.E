import React from 'react';

export const MetricCard = ({ title, value, subtitle, colorScheme = 'blue' }) => {
  const colorMap = {
    blue: 'border-l-blue-600',
    green: 'border-l-teal-600',
    amber: 'border-l-amber-600',
    slate: 'border-l-slate-700',
    red: 'border-l-rose-600'
  };

  const leftBorderColor = colorMap[colorScheme] || colorMap['slate'];

  return (
    <div className={`bg-white border border-[#EAE8E2] ${leftBorderColor} border-l-[4px] p-6 shadow-sm`}>
      <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-widest mb-2">
        {title}
      </h3>
      <div className="text-4xl font-light text-slate-900 mb-1">
        {value}
      </div>
      {subtitle && (
        <p className="text-sm text-slate-400">
          {subtitle}
        </p>
      )}
    </div>
  );
};
