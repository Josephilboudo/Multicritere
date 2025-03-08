
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  // Réinitialiser le formulaire pour l'ajout
  function resetForm() {
      document.getElementById('elementForm').reset();
      document.getElementById('formAction').value = 'add';
      document.getElementById('codeElement').readOnly = false;
      document.getElementById('elementModalLabel').textContent = 'Ajouter un élément';
  }
  
  // Préremplir le formulaire pour la modification
  function editElement(code, description) {
      document.getElementById('formAction').value = 'edit';
      document.getElementById('codeElement').value = code;
      document.getElementById('codeElement').readOnly = true;
      document.getElementById('description').value = description;
      document.getElementById('elementModalLabel').textContent = 'Modifier un élément';
      
      var modal = new bootstrap.Modal(document.getElementById('elementModal'));
      modal.show();
  }
  
  // Obtenir le token CSRF
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  
  // Configurer la suppression
  function deleteElement(code) {
      document.getElementById('confirmDeleteButton').setAttribute('data-code', code);
      var modal = new bootstrap.Modal(document.getElementById('deleteModal'));
      modal.show();
  }
  
  // Afficher un toast
  function showToast(message, type) {
      const toastContainer = document.querySelector('.toast-container');
      const toast = document.createElement('div');
      toast.classList.add('toast', 'show');
      toast.setAttribute('role', 'alert');
      toast.setAttribute('aria-live', 'assertive');
      toast.setAttribute('aria-atomic', 'true');
      
      toast.innerHTML = `
          <div class="toast-header bg-${type} text-white">
              <strong class="me-auto">Notification</strong>
              <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
          </div>
          <div class="toast-body">
              ${message}
          </div>
      `;
      
      toastContainer.appendChild(toast);
      
      setTimeout(() => {
          const bsToast = new bootstrap.Toast(toast);
          bsToast.hide();
          setTimeout(() => {
              toast.remove();
          }, 500);
      }, 5000);
  }
  
  // Construire le HTML du tableau à partir des données JSON
  function buildTableHTML(elements) {
      let html = `
          <table class="table table-striped">
              <thead>
                  <tr>
                      <th>Code</th>
                      <th>Description</th>
                      <th>Actions</th>
                  </tr>
              </thead>
              <tbody>`;
      
      if (elements.length === 0) {
          html += `
              <tr>
                  <td colspan="3" class="text-center">Aucun élément disponible</td>
              </tr>`;
      } else {
          elements.forEach(element => {
              html += `
                  <tr>
                      <td>${element.codeElement}</td>
                      <td>${element.description}</td>
                      <td>
                          <button class="btn btn-info btn-sm" onclick="editElement('${element.codeElement}', '${element.description}')">
                              <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-danger btn-sm" onclick="deleteElement('${element.codeElement}')">
                              <i class="fas fa-trash"></i>
                          </button>
                      </td>
                  </tr>`;
          });
      }
      
      html += `
              </tbody>
          </table>`;
      
      return html;
  }
  
  // Recharger la liste des éléments
  function refreshElementList() {
      fetch('{% url "get_elements_json" %}')
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  const tableHTML = buildTableHTML(data.elements);
                  document.getElementById('element-list-container').innerHTML = tableHTML;
              } else {
                  showToast('Erreur lors du chargement des données', 'danger');
              }
          })
          .catch(error => {
              console.error('Erreur lors du rechargement de la liste:', error);
              showToast('Erreur lors du rechargement de la liste', 'danger');
          });
  }
  
  // Fonction pour nettoyer les modals et backdrops
  function cleanupModals() {
      // Supprime toutes les modal-backdrop
      document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
      
      // Réinitialise le body
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
  }
  
  // Force la fermeture d'un modal
  function forceCloseModal(modalElement) {
      if (!modalElement) return;
      
      // Essayez de récupérer l'instance Bootstrap
      let modalInstance = bootstrap.Modal.getInstance(modalElement);
      
      if (modalInstance) {
          // Si l'instance existe, utilisez la méthode hide
          modalInstance.hide();
      } else {
          // Si l'instance n'existe pas, fermez manuellement
          modalElement.classList.remove('show');
          modalElement.setAttribute('aria-hidden', 'true');
          modalElement.style.display = 'none';
      }
      
      // Nettoyez après tout ça pour être sûr
      setTimeout(cleanupModals, 300);
  }
  
  // Configurer les événements au chargement de la page
  document.addEventListener('DOMContentLoaded', function() {
      const csrfToken = getCookie('csrftoken');
      
      // Nettoyez les modals au chargement
      cleanupModals();
      
      // Gestionnaire pour le bouton Enregistrer
      document.getElementById('saveButton').addEventListener('click', function() {
          const form = document.getElementById('elementForm');
          const formData = new FormData(form);
          const elementModal = document.getElementById('elementModal');
          
          fetch('{% url "save_element" %}', {
              method: 'POST',
              headers: {
                  'X-CSRFToken': csrfToken
              },
              body: formData
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  showToast(data.message, 'success');
                  refreshElementList();
                  
                  // Fermer de force le modal
                  forceCloseModal(elementModal);
              } else {
                  showToast(data.message, 'danger');
              }
          })
          .catch(error => {
              console.error('Erreur:', error);
              showToast('Une erreur est survenue', 'danger');
          });
      });
      
      // Gestionnaire pour le bouton Supprimer
      document.getElementById('confirmDeleteButton').addEventListener('click', function() {
          const code = this.getAttribute('data-code');
          const deleteModal = document.getElementById('deleteModal');
          
          const formData = new FormData();
          formData.append('codeElement', code);
          
          fetch('{% url "delete_element" %}', {
              method: 'POST',
              headers: {
                  'X-CSRFToken': csrfToken
              },
              body: formData
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  showToast(data.message, 'success');
                  refreshElementList();
                  
                  // Fermer de force le modal
                  forceCloseModal(deleteModal);
              } else {
                  showToast(data.message, 'danger');
              }
          })
          .catch(error => {
              console.error('Erreur:', error);
              showToast('Une erreur est survenue', 'danger');
          });
      });
  });
