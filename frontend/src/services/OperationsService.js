import instance from "@/services/MainService";

export default {
  extract(store) {
    return new Promise((resolve, reject) => {
      var formData = new FormData();
      var project = {
        project_name: store.state.project_name,
        description: store.state.description,
        author: store.state.user,
        user_id: store.state.user_id,
        creation_date: new Date(),
      };
      formData.append("project", JSON.stringify(project));
      formData.append("file", store.state.file_uploaded);
      formData.append("user_id", store.state.user_id);
      formData.append("project_name", store.state.project_name);
      formData.append("description", store.state.description);
      formData.append("separator", store.state.csv.separator);
      formData.append("tables", store.state.html.extract_tables);
      formData.append("paragraphs", store.state.html.extract_paragraphs);
      console.log(project);
      instance
        .post("extract/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log(response.data);
          store.state.project_id = response.data.project_id;
          store.state.filename = response.data.filename;
          store.state.file_type = response.data.type;
          store.state.size = response.data.size;

          if (response.data.type == "csv") {
            store.state.csv.headers = response.data.results.headers;
            store.state.csv.columns = response.data.results.columns;
            store.state.csv.lines = response.data.results.lines;
          }
          if (
            response.data.type == "html" ||
            response.data.type == "pdf" ||
            response.data.type == "image"
          ) {
            store.state.html.tables = response.data.results.tables;
            store.state.html.paragraphs = response.data.results.paragraphs;
            store.state.html.num_paragraphs =
              response.data.results.num_paragraphs;
            store.state.html.num_tables = response.data.results.num_tables;
          }
          if (response.data.type == "text") {
            store.state.text.paragraph = response.data.results.paragraph;
            store.state.text.sentences = response.data.results.sentences;
          }

          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  preprocess(store) {
    return new Promise((resolve, reject) => {
      var formData = new FormData();
      formData.append("project_id", store.state.project_id);
      formData.append("file_type", store.state.file_type);

      if (store.state.file_type == "csv") {
        formData.append("columns", JSON.stringify(store.state.csv.headers));
      }

      if (
        store.state.file_type == "html" ||
        store.state.file_type == "pdf" ||
        store.state.file_type == "image"
      ) {
        formData.append("tables", JSON.stringify(store.state.html.tables));
        formData.append(
          "paragraphs",
          JSON.stringify(store.state.html.paragraphs)
        );
      }
      if (store.state.file_type == "text") {
        formData.append("paragraph", JSON.stringify(store.state.text));
      }

      instance
        .post("preprocess/", formData)
        .then((response) => {
          console.log(response.data);

          if (store.state.file_type == "csv") {
            store.state.csv.headers = response.data.headers;
          }
          if (
            store.state.file_type == "html" ||
            store.state.file_type == "pdf" ||
            store.state.file_type == "image"
          ) {
            store.state.html.tables = response.data.tables_selected;
            store.state.html.paragraphs = response.data.paragraphs_selected;
          }
          if (store.state.file_type == "text") {
            store.state.text.paragraph = response.data.data;
          }
          resolve(response);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
  explore(store) {
    return new Promise((resolve, reject) => {
      var formData = new FormData();
      formData.append("file_type", store.state.file_type);
      formData.append("vocabs", JSON.stringify(store.state.vocabs));
      formData.append("project_id", store.state.project_id);

      if (store.state.file_type == "csv") {
        formData.append("columns", JSON.stringify(store.state.csv.headers));
      }
      if (
        store.state.file_type == "html" ||
        store.state.file_type == "pdf" ||
        store.state.file_type == "image"
      ) {
        formData.append("tables", JSON.stringify(store.state.html.tables));
        formData.append(
          "paragraphs",
          JSON.stringify(store.state.html.paragraphs)
        );
      }
      if (store.state.file_type == "text") {
        formData.append(
          "paragraph",
          JSON.stringify(store.state.text.paragraph)
        );
      }

      instance
        .post("explore/", formData)
        .then((response) => {
          console.log(response.data);
          if (store.state.file_type == "csv") {
            store.state.csv.terms = response.data.terms;
            console.log(response.data);
          }
          if (
            store.state.file_type == "html" ||
            store.state.file_type == "pdf" ||
            store.state.file_type == "image"
          ) {
            store.state.html.tables = response.data.tables;
            store.state.html.paragraphs = response.data.paragraphs;
          }
          if (store.state.file_type == "text") {
            store.state.text.paragraph = response.data.data;
          }

          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  convert(store) {
    return new Promise((resolve, reject) => {
      var formData = new FormData();
      console.log("here");
      formData.append("file_type", store.state.file_type);
      formData.append("project_id", store.state.project_id);
      formData.append("file_name", store.state.filename);
      if (store.state.file_type == "csv") {
        formData.append("delimiter", store.state.csv.separator);
        var terms = [];
        store.state.csv.terms.forEach(function(term) {
          terms.push({
            property: term.property,
            term: term.selected,
            type: term.type,
          });
        });
        formData.append("rowClass", JSON.stringify(store.state.csv.rowClass));
        var headersId = [];
        store.state.csv.headersId.forEach((header) => {
          headersId.push(header.property);
        });
        formData.append("headersId", JSON.stringify(headersId));
        formData.append("terms", JSON.stringify(terms));
      }
      if (store.state.file_type == "text") {
        var triplets = [];
        store.state.text.paragraph.sentences.forEach(function(sentence) {
          sentence.triplets.forEach(function(triplet) {
            triplets.push(triplet);
          });
        });
        terms = [];

        store.state.text.paragraph.terms.forEach(function(term) {
          terms.push({
            property: term.property,
            term: term.selected,
            type: term.type,
          });
        });
        formData.append("terms", JSON.stringify(terms));
        formData.append("triplets", JSON.stringify(triplets));
        formData.append(
          "entities",
          JSON.stringify(store.state.text.paragraph.entities)
        );
      }
      if (
        store.state.file_type == "html" ||
        store.state.file_type == "pdf" ||
        store.state.file_type == "image"
      ) {
        var tables = [];
        store.state.html.tables.forEach(function(table) {
          if (table.selected) {
            var filename = table.filename;
            var id = table.id;
            var terms = [];
            table.terms.forEach(function(term) {
              terms.push({
                property: term.property,
                term: term.selected,
                type: term.type,
              });
            });
            tables.push({
              filename: filename,
              id: id,
              terms: terms,
              rowId: table.rowId,
              rowClass: table.rowClass,
            });
          }
        });
        var paragraphs = [];
        store.state.html.paragraphs.forEach(function(paragraph) {
          if (paragraph.selected) {
            var id = paragraph.id;
            var terms = [];
            var triplets = [];
            var entities = [];
            paragraph.terms.forEach(function(term) {
              terms.push({
                property: term.property,
                term: term.selected,
              });
            });
            paragraph.sentences.forEach(function(sentence) {
              sentence.triplets.forEach(function(triplet) {
                if (triplet.selected) triplets.push(triplet);
              });
              paragraph.entities.forEach(function(entity) {
                console.log(entity);
                if (entity.selected) entities.push(entity);
              });
            });

            paragraphs.push({
              id: id,
              terms: terms,
              triplets: triplets,
              entities: entities,
            });
          }
        });

        formData.append("tables", JSON.stringify(tables));
        formData.append("paragraphs", JSON.stringify(paragraphs));
      }
      instance
        .post("convert/", formData)
        .then((response) => {
          console.log(response.data);
          if (store.state.file_type == "csv") {
            store.state.csv.triplets = response.data.data;
          }
          if (store.state.file_type == "text") {
            store.state.text.triplets = response.data.data;
          }
          if (
            store.state.file_type == "html" ||
            store.state.file_type == "pdf" ||
            store.state.file_type == "image"
          ) {
            store.state.html.tables_triplets = response.data.tables;
            store.state.html.paragraphs_triplets = response.data.paragraphs;
          }
          resolve(response);
        })
        .catch((error) => {
          console.log(error);
          reject(error);
        });
    });
  },
  document(store, format) {
    return new Promise((resolve, reject) => {
      var formData = new FormData();
      console.log("project_id" + store.state.project_id);
      formData.append("metadata", JSON.stringify(store.state.metadata));
      formData.append("project_id", store.state.project_id);
      formData.append("format", format);
      instance
        .post("document/", formData)
        .then((response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
