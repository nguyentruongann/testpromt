export default [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",     
      sourceType: "module",       
    },
    rules: {
      "no-unused-vars": "warn",  
      "no-undef": "error",       
      "no-console": "off",        
      "eqeqeq": ["error", "always"],
      "semi": ["error", "always"],   
      "quotes": ["error", "double"], 
    },
  },
];
