import { useEffect, useState, React } from 'react';
import { Form, Container, Row, Button } from 'react-bootstrap';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';

let text_url = "http://localhost:5000/predict_text";
let pdf_url = "http://localhost:5000/predict_pdf";
let url_url = "http://localhost:5000/predict_url";

async function sendRequest() {
  const headers = {
    'Content-Type': 'application/json'
  };

  const body = {
    "vacancy_text": "text dfrfycbb"
  };

  const response = await axios.post(text_url, body, { headers });
  console.log(response.data);
  return response;
}

export default function FormVacancy() {
  const [isLoading, setLoading] = useState(false);
  //const [data, setData] = useState({ hits: []})
  const [data, setData] = useState('')

  useEffect(() => {
    if (isLoading) {
      sendRequest().then(() => {
        setLoading(false);
      });
    }
  }, [isLoading]);

  const handleClick = () => setLoading(true);

  const onFormSubmit = e => {
    e.preventDefault()
    if (e.target['ref'].value.trim() !== '') {
      setData(e.target['ref'].value.trim());
    } else if (e.target['pdf'].value.trim() !== '') {
      setData(e.target['pdf'].value.trim())
    } else if (e.target['txt'].value.trim() !== '') {
      setData(e.target['txt'].value.trim())
    }
    console.log(data)
    //console.log(e.target['ref'].value)
    //console.log(e.target['pdf'].value)
    //console.log(e.target['txt'].value)
  }

  return (
    <div>
      <Form onSubmit={onFormSubmit}>
        <Form.Group className="mb-3">
          <Container>
            <Row>
              <Form.Label>
                Вставьте ссылку на вакансию:
              </Form.Label>
              <br />
              <Form.Control size="lg" type="text" placeholder="URL вакансии" id='ref'/>
            </Row>
            <br />
            <Row>
              <Form.Label id='pdf'>Или загрузите PDF вакансии:</Form.Label>
              <br />
              <Form.Control size="lg" type="file" id='pdf'/>
            </Row>
            <br />
            <Row>
              <Form.Label id='txt'>Или вставьте текст вакансии:</Form.Label>
              <br />
              <Form.Label></Form.Label>
              <Form.Control as="textarea" rows={5} id='txt'/>
            </Row>
            <br />
            <Row>
              <Button variant="primary" 
                type="submit" 
                disabled={isLoading}
                onClick={!isLoading ? 
                  (e) => handleClick : null}
              >
                {isLoading ? 'Загрузка…' : 'Начать поиск'}
              </Button>
            </Row>
          </Container>
        </Form.Group>
      </Form>        
    </div>
  )
}
