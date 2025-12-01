export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const formatNumber = (number) => {
  return new Intl.NumberFormat().format(number);
};

export const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};
