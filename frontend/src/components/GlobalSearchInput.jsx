import React, { useState } from 'react';
import { Form, InputGroup, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const GlobalSearchInput = () => {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <Form onSubmit={handleSearch} className="d-flex me-2 my-1 my-xl-0">
      <InputGroup size="sm" style={{ minWidth: '130px', maxWidth: '200px' }}>
        <Form.Control
          type="search"
          placeholder="Global Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button variant="outline-light" type="submit">
          🔍
        </Button>
      </InputGroup>
    </Form>
  );
};

export default GlobalSearchInput;
