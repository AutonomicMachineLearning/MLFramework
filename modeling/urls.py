from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from modeling.views import *

urlpatterns = [
    #url('$', ModelingView_model.as_view()),


    url('data/$', ModelingView_data.as_view()),
    url('model/$', FileUploadView.as_view(), name='model_base'),
    url('hyperparameter/$', ModelingView_hyperparameter.as_view()),
    url('training/$', ModelingView_Training.as_view()),
    url('result/$', ModelingView_Result.as_view()),
    url('inference/$', ModelingView_Inference.as_view()),

    # Ajax access
    # url('data/dataset_list/$', getDatasetList),
    url('data/table/', getTable),
    url('model/save/$', setModelSequence),

    # Ajax access - training
    url('training/getTrainingResult/$', getTrainingResult),
    url('result/getResultAll/$', select_result),

    url('modelTest/$', Testview.as_view())
]